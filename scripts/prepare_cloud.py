from pathlib import Path


def patch_backend():
    path = Path("backend/main.py")
    text = path.read_text(encoding="utf-8")

    if "import os\n" not in text:
        text = text.replace("from io import BytesIO\n", "from io import BytesIO\nimport os\n", 1)

    old_constants = '''OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "bge-m3"
ANSWER_MODEL = "qwen3:8b"
TIMEOUT = 300.0
'''
    new_constants = '''GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
EMBEDDING_MODEL = "gemini-embedding-2"
ANSWER_MODEL = "gemini-3.7-flash"
EMBEDDING_DIMENSIONS = 768
TIMEOUT = 300.0

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
'''
    if old_constants in text:
        text = text.replace(old_constants, new_constants, 1)

    text = text.replace(
        'description="Free local multilingual RAG powered by Ollama",',
        'description="Cloud-ready multilingual RAG powered by Gemini",',
    )
    text = text.replace(
        'allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],',
        'allow_origins=ALLOWED_ORIGINS,',
    )

    start = text.find("def check_ollama():")
    end = text.find("def cosine_similarity", start)
    if start != -1 and end != -1:
        gemini_helpers = '''def gemini_headers():
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
        prepared = [f"task: retrieval_query | query: {item}" for item in texts]
    else:
        prepared = [f"task: retrieval_document | document: {item}" for item in texts]

    result = []
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            for i in range(0, len(prepared), 20):
                batch = prepared[i:i + 20]
                payload = {
                    "requests": [
                        {
                            "model": f"models/{EMBEDDING_MODEL}",
                            "content": {"parts": [{"text": item}]},
                            "outputDimensionality": EMBEDDING_DIMENSIONS,
                        }
                        for item in batch
                    ]
                }
                response = client.post(
                    f"{GEMINI_BASE_URL}/models/{EMBEDDING_MODEL}:batchEmbedContents",
                    headers=gemini_headers(),
                    json=payload,
                )
                response.raise_for_status()
                embeddings = response.json().get("embeddings", [])
                if len(embeddings) != len(batch):
                    raise RuntimeError("Unexpected embeddings response from Gemini")
                result.extend(item["values"] for item in embeddings)
        return result
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
    full_prompt = f"{system_prompt}\\n\\n---\\n\\n{user_prompt}"
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
                        "maxOutputTokens": 2048,
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


'''
        text = text[:start] + gemini_helpers + text[end:]

    text = text.replace(
        'q = create_embeddings([question])[0]',
        'q = create_embeddings([question], task="query")[0]',
    )

    old_search = '''    results = []
    for chunk in candidates:
        results.append({**chunk, "similarity": cosine_similarity(q, chunk["embedding"])})
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
'''
    new_search = '''    results = []
    for chunk in candidates:
        similarity = cosine_similarity(q, chunk["embedding"])
        lexical_boost = field_intent_boost(question, chunk["text"])
        results.append({
            **chunk,
            "similarity": similarity,
            "hybrid_score": similarity + lexical_boost,
        })
    results.sort(key=lambda x: x["hybrid_score"], reverse=True)
    return results[:top_k]
'''
    if old_search in text:
        text = text.replace(old_search, new_search, 1)

    text = text.replace('"message": "DocMind AI API is running locally",', '"message": "DocMind AI API is running",')
    text = text.replace('"ai_provider": "Ollama",', '"ai_provider": "Gemini API",')
    text = text.replace('"ollama_connected": check_ollama(),', '"gemini_configured": check_gemini(),')
    text = text.replace('answer = ollama_chat(system_prompt, user_prompt)', 'answer = gemini_chat(system_prompt, user_prompt)')
    text = text.replace('summary = ollama_chat(system_prompt, "".join(parts))', 'summary = gemini_chat(system_prompt, "".join(parts))')
    text = text.replace('version="3.1.0"', 'version="4.0.0"')
    text = text.replace('"version": "3.1.0"', '"version": "4.0.0"')
    text = text.replace('version="3.2.0"', 'version="4.0.0"')
    text = text.replace('"version": "3.2.0"', '"version": "4.0.0"')

    path.write_text(text, encoding="utf-8")


def patch_frontend():
    path = Path("frontend/app/page.tsx")
    text = path.read_text(encoding="utf-8")

    if "const API_BASE_URL" not in text:
        text = text.replace(
            'import { useRef, useState } from "react";\n',
            'import { useRef, useState } from "react";\n\nconst API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";\n',
            1,
        )

    text = text.replace('powered: "Powered locally by Ollama",', 'powered: "Powered by Gemini",')
    text = text.replace('powered: "يعمل محليًا باستخدام Ollama",', 'powered: "مدعوم بواسطة Gemini",')
    text = text.replace('fetch("http://localhost:8000/upload",', 'fetch(`${API_BASE_URL}/upload`,')
    text = text.replace('fetch("http://localhost:8000/ask",', 'fetch(`${API_BASE_URL}/ask`,')

    path.write_text(text, encoding="utf-8")


def create_deploy_files():
    Path("backend/requirements.txt").write_text(
        """fastapi>=0.115,<1.0
uvicorn[standard]>=0.34,<1.0
python-multipart>=0.0.20,<1.0
pypdf>=5.0,<7.0
python-docx>=1.1,<2.0
python-pptx>=1.0,<2.0
numpy>=2.0,<3.0
httpx>=0.28,<1.0
""",
        encoding="utf-8",
    )

    Path("render.yaml").write_text(
        """services:
  - type: web
    name: docmind-ai-api
    runtime: python
    rootDir: backend
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: ALLOWED_ORIGINS
        sync: false
""",
        encoding="utf-8",
    )


patch_backend()
patch_frontend()
create_deploy_files()
print("DocMind cloud deployment files prepared.")
