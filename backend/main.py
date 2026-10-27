from io import BytesIO
import os
import re
from pathlib import Path
from typing import Annotated
from uuid import uuid4

import httpx
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pypdf import PdfReader
from docx import Document
from pptx import Presentation

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
EMBEDDING_MODEL = "gemini-embedding-2"
ANSWER_MODEL = "gemini-3.8-flash"
EMBEDDING_DIMENSIONS = 768
TIMEOUT = 300.0
MAX_FILE_BYTES = 10 * 1024 * 1024

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
if allowed_origins_env:
    ALLOWED_ORIGINS.extend(
        origin.strip()
        for origin in allowed_origins_env.split(",")
        if origin.strip()
    )

app = FastAPI(
    title="DocMind AI API",
    description="Cloud-ready multilingual RAG powered by Gemini",
    version="4.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCUMENTS: dict[str, dict] = {}
CHUNKS: list[dict] = []


class AskRequest(BaseModel):
    question: str = Field(min_length=2)
    document_ids: list[str] | None = None
    top_k: int = Field(default=5, ge=1, le=10)


class SearchRequest(BaseModel):
    question: str = Field(min_length=2)
    document_ids: list[str] | None = None
    top_k: int = Field(default=5, ge=1, le=10)


class SummaryRequest(BaseModel):
    document_ids: list[str] | None = None
    language: str = "auto"


def gemini_headers():
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured on the server.",
        )

    return {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }


def check_gemini():
    return bool(GEMINI_API_KEY)


def create_embeddings(texts: list[str], task: str = "document"):
    if not texts:
        return []

    if task == "query":
        prepared = [f"task: retrieval_query | query: {text}" for text in texts]
    else:
        prepared = [f"task: retrieval_document | document: {text}" for text in texts]

    vectors = []

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            for text in prepared:
                response = client.post(
                    f"{GEMINI_BASE_URL}/models/{EMBEDDING_MODEL}:embedContent",
                    headers=gemini_headers(),
                    json={
                        "model": f"models/{EMBEDDING_MODEL}",
                        "content": {
                            "parts": [{"text": text}],
                        },
                        "output_dimensionality": EMBEDDING_DIMENSIONS,
                    },
                )
                response.raise_for_status()

                embedding = response.json().get("embedding", {}).get("values", [])
                if not embedding:
                    raise RuntimeError("Gemini returned an empty embedding")

                vectors.append(embedding)

        return vectors

    except httpx.HTTPStatusError as error:
        print("Gemini embedding HTTP error:", error.response.text)
        raise HTTPException(
            status_code=502,
            detail="Gemini embedding request failed. Check the API key and free-tier quota.",
        )
    except HTTPException:
        raise
    except Exception as error:
        print("Embedding error:", repr(error))
        raise HTTPException(502, "Could not create document embeddings.")


def gemini_chat(system_prompt: str, user_prompt: str):
    full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            response = client.post(
                f"{GEMINI_BASE_URL}/models/{ANSWER_MODEL}:generateContent",
                headers=gemini_headers(),
                json={
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": full_prompt}],
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.0,
                        "maxOutputTokens": 1600,
                        "thinkingConfig": {
                            "thinkingLevel": "low"
                        },
                    },
                },
            )
            response.raise_for_status()

            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                raise RuntimeError("Gemini returned no candidates")

            parts = candidates[0].get("content", {}).get("parts", [])
            answer = "".join(part.get("text", "") for part in parts).strip()

            if not answer:
                raise RuntimeError("Gemini returned an empty answer")

            return answer

    except httpx.HTTPStatusError as error:
        print("Gemini chat HTTP error:", error.response.text)
        raise HTTPException(
            status_code=502,
            detail="Gemini answer request failed. Check the API key and free-tier quota.",
        )
    except HTTPException:
        raise
    except Exception as error:
        print("Chat error:", repr(error))
        raise HTTPException(502, "Could not generate an AI answer.")


def cosine_similarity(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    return 0.0 if denominator == 0 else float(np.dot(a, b) / denominator)


def extract_pdf(data: bytes):
    reader = PdfReader(BytesIO(data))
    output = []

    for page_number, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if text:
            output.append(
                {
                    "location": f"Page {page_number}",
                    "location_number": page_number,
                    "text": text,
                }
            )

    return output


def extract_docx(data: bytes):
    document = Document(BytesIO(data))
    output = []
    paragraph_number = 0

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraph_number += 1
            output.append(
                {
                    "location": f"Paragraph {paragraph_number}",
                    "location_number": paragraph_number,
                    "text": text,
                }
            )

    return output


def extract_pptx(data: bytes):
    presentation = Presentation(BytesIO(data))
    output = []

    for slide_number, slide in enumerate(presentation.slides, 1):
        parts = []

        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text = shape.text.strip()
                if text:
                    parts.append(text)

        if parts:
            output.append(
                {
                    "location": f"Slide {slide_number}",
                    "location_number": slide_number,
                    "text": "\n".join(parts),
                }
            )

    return output


def chunk_text(text: str, max_chars=1400, overlap=250):
    text = text.strip()
    if not text:
        return []

    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + max_chars, len(text))

        if end < len(text):
            search_start = start + int(max_chars * 0.60)
            section = text[search_start:end]
            break_points = [
                section.rfind("\n"),
                section.rfind(". "),
                section.rfind("? "),
                section.rfind("! "),
                section.rfind("، "),
                section.rfind("؟ "),
            ]
            best_break = max(break_points)

            if best_break > 0:
                end = search_start + best_break + 1

        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def create_document_chunks(document_id: str, filename: str, locations: list):
    output = []

    for location in locations:
        for piece_number, piece in enumerate(chunk_text(location["text"]), 1):
            output.append(
                {
                    "id": str(uuid4()),
                    "document_id": document_id,
                    "filename": filename,
                    "location": location["location"],
                    "location_number": location["location_number"],
                    "piece_number": piece_number,
                    "text": piece,
                    "embedding": None,
                }
            )

    return output


FIELD_INTENTS = [
    {
        "question_terms": ["الاسم", "اسم", "name", "full name"],
        "document_terms": ["personal information", "full name", "name"],
    },
    {
        "question_terms": ["الجامعة", "جامعة", "university", "college"],
        "document_terms": ["university", "college", "education"],
    },
    {
        "question_terms": ["الجوال", "الهاتف", "رقم الجوال", "phone", "mobile", "telephone"],
        "document_terms": ["phone number", "phone", "mobile", "telephone"],
    },
    {
        "question_terms": ["البريد", "الايميل", "الإيميل", "email", "e-mail"],
        "document_terms": ["e-mail", "email"],
    },
    {
        "question_terms": ["الجنسية", "nationality"],
        "document_terms": ["nationality"],
    },
    {
        "question_terms": ["الموقع", "المدينة", "location", "city"],
        "document_terms": ["location", "city"],
    },
    {
        "question_terms": ["التخصص", "major", "specialization"],
        "document_terms": ["major", "computer science", "specialization", "faculty"],
    },
    {
        "question_terms": ["الخبرات", "الخبرة", "experience", "work experience"],
        "document_terms": ["experience", "work", "internship", "training"],
    },
    {
        "question_terms": ["المهارات", "skills", "skill"],
        "document_terms": ["skills", "skill"],
    },
]


def field_intent_boost(question: str, text: str) -> float:
    question_lower = question.lower()
    text_lower = text.lower()
    best_boost = 0.0

    for intent in FIELD_INTENTS:
        if any(term in question_lower for term in intent["question_terms"]):
            if any(term in text_lower for term in intent["document_terms"]):
                best_boost = max(best_boost, 0.22)

    return best_boost


def semantic_search(question: str, document_ids=None, top_k=5):
    if not CHUNKS:
        raise HTTPException(400, "No processed documents found. Upload documents first.")

    if not document_ids:
        raise HTTPException(400, "Select at least one uploaded document.")

    candidates = [
        chunk
        for chunk in CHUNKS
        if chunk["document_id"] in document_ids
    ]

    if not candidates:
        raise HTTPException(404, "No chunks found for the selected documents.")

    query_embedding = create_embeddings([question], task="query")[0]
    results = []

    for chunk in candidates:
        similarity = cosine_similarity(query_embedding, chunk["embedding"])
        lexical_boost = field_intent_boost(question, chunk["text"])

        results.append(
            {
                **chunk,
                "similarity": similarity,
                "hybrid_score": similarity + lexical_boost,
            }
        )

    results.sort(key=lambda item: item["hybrid_score"], reverse=True)
    return results[:top_k]


@app.get("/")
def root():
    return {
        "message": "DocMind AI API is running",
        "version": "4.1.0",
        "ai_provider": "Gemini API",
        "embedding_model": EMBEDDING_MODEL,
        "answer_model": ANSWER_MODEL,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "gemini_configured": check_gemini(),
        "embedding_model": EMBEDDING_MODEL,
        "answer_model": ANSWER_MODEL,
    }


@app.post("/upload")
async def upload_documents(
    files: Annotated[
        list[UploadFile],
        File(description="Upload PDF, DOCX, or PPTX files"),
    ]
):
    uploaded = []

    for file in files:
        if not file.filename:
            continue

        extension = Path(file.filename).suffix.lower()
        if extension not in [".pdf", ".docx", ".pptx"]:
            raise HTTPException(400, f"Unsupported file type: {extension}")

        data = await file.read()
        if len(data) > MAX_FILE_BYTES:
            raise HTTPException(413, f"{file.filename} is larger than 10 MB.")

        try:
            if extension == ".pdf":
                locations = extract_pdf(data)
            elif extension == ".docx":
                locations = extract_docx(data)
            else:
                locations = extract_pptx(data)
        except Exception as error:
            print("Extraction error:", file.filename, repr(error))
            raise HTTPException(400, f"Could not read {file.filename}")

        if not locations:
            raise HTTPException(
                400,
                f"No readable text was found in {file.filename}. Scanned PDFs need OCR support.",
            )

        document_id = str(uuid4())
        document_chunks = create_document_chunks(
            document_id,
            file.filename,
            locations,
        )

        embeddings = create_embeddings(
            [chunk["text"] for chunk in document_chunks],
            task="document",
        )

        for chunk, embedding in zip(document_chunks, embeddings):
            chunk["embedding"] = embedding

        DOCUMENTS[document_id] = {
            "id": document_id,
            "filename": file.filename,
            "file_type": extension.replace(".", ""),
            "locations": locations,
        }
        CHUNKS.extend(document_chunks)

        uploaded.append(
            {
                "id": document_id,
                "filename": file.filename,
                "file_type": extension.replace(".", ""),
                "locations_found": len(locations),
                "characters_extracted": sum(
                    len(location["text"])
                    for location in locations
                ),
                "chunks_created": len(document_chunks),
                "preview": locations[0]["text"][:250],
            }
        )

    return {
        "success": True,
        "documents": uploaded,
    }


@app.post("/search")
def search_documents(request: SearchRequest):
    results = semantic_search(
        request.question,
        request.document_ids,
        request.top_k,
    )

    return {
        "question": request.question,
        "results": [
            {
                "document_id": result["document_id"],
                "filename": result["filename"],
                "location": result["location"],
                "similarity": round(result["similarity"], 4),
                "text": result["text"],
            }
            for result in results
        ],
    }


@app.post("/ask")
def ask_documents(request: AskRequest):
    results = semantic_search(
        request.question,
        request.document_ids,
        request.top_k,
    )

    context_parts = []
    sources = []

    for source_number, result in enumerate(results, 1):
        context_parts.append(
            f'[SOURCE {source_number}]\n'
            f'File: {result["filename"]}\n'
            f'Location: {result["location"]}\n\n'
            f'{result["text"]}'
        )

        sources.append(
            {
                "source_number": source_number,
                "document_id": result["document_id"],
                "filename": result["filename"],
                "location": result["location"],
                "similarity": round(result["similarity"], 4),
                "preview": result["text"][:300],
            }
        )

    system_prompt = """
You are DocMind AI, a strict document-grounded assistant.

RULES:
1. Use ONLY facts explicitly written in the retrieved document context.
2. Do not infer, guess, complete, or add outside knowledge.
3. For names, phone numbers, emails, universities, nationality, dates, IDs,
   and locations, copy the exact value from the source text.
4. A project description is not evidence for an unrelated personal fact.
5. If the requested information is not explicitly present, say that it was not
   found in the uploaded documents and do not cite a source.
6. Answer in the same language as the user's question unless asked otherwise.
7. Translation is allowed, but exact names, numbers, emails, and identifiers
   must remain exactly as written in the source.
8. Cite factual answers with [1], [2], etc.
9. Cite only sources that directly support the answer.
10. Keep simple factual answers concise.
11. Do not use Markdown bold, headings, or tables. Use plain text or simple lists.
""".strip()

    user_prompt = f"""
USER QUESTION:
{request.question}

RETRIEVED DOCUMENT CONTEXT:
{chr(10).join(context_parts)}

Answer using only the context above.
""".strip()

    answer = gemini_chat(system_prompt, user_prompt)

    not_found_phrases = [
        "لم أجد",
        "غير موجود",
        "غير مذكور",
        "غير مذكورة",
        "لا توجد معلومات",
        "لا يوجد معلومات",
        "could not find",
        "couldn't find",
        "not found",
        "not mentioned",
        "no information",
    ]

    is_not_found = any(
        phrase.lower() in answer.lower()
        for phrase in not_found_phrases
    )

    if is_not_found:
        answer = re.sub(r"\s*\[\d+\]", "", answer).strip()
        cited_sources = []
    else:
        cited_numbers = {
            int(number)
            for number in re.findall(r"\[(\d+)\]", answer)
        }
        cited_sources = [
            source
            for source in sources
            if source["source_number"] in cited_numbers
        ]

    return {
        "question": request.question,
        "answer": answer,
        "sources": cited_sources,
    }


@app.post("/summarize")
def summarize_documents(request: SummaryRequest):
    if not request.document_ids:
        raise HTTPException(400, "Select at least one uploaded document.")

    selected = [
        document
        for document_id, document in DOCUMENTS.items()
        if document_id in request.document_ids
    ]

    if not selected:
        raise HTTPException(404, "No documents found to summarize.")

    parts = []
    total_characters = 0
    max_characters = 70000

    for document in selected:
        parts.append(f'\n=== FILE: {document["filename"]} ===\n')

        for location in document["locations"]:
            section = (
                f'\n{location["location"]}:\n'
                f'{location["text"]}\n'
            )

            if total_characters + len(section) > max_characters:
                break

            parts.append(section)
            total_characters += len(section)

        if total_characters >= max_characters:
            break

    language = request.language.lower()

    if language == "arabic":
        language_instruction = "Write the summary in Arabic."
    elif language == "english":
        language_instruction = "Write the summary in English."
    else:
        language_instruction = "Write the summary in the main language of the documents."

    system_prompt = f"""
You are DocMind AI.
Summarize ONLY the supplied documents. Do not add outside knowledge.
Create a clear structured summary with the main ideas, key facts,
important definitions when present, and conclusions when present.
{language_instruction}
""".strip()

    summary = gemini_chat(system_prompt, "".join(parts))

    return {
        "summary": summary,
        "documents": [
            {
                "id": document["id"],
                "filename": document["filename"],
            }
            for document in selected
        ],
    }
