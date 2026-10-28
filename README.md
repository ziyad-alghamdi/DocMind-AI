<p align="center">
  <strong>English</strong> · <a href="README_AR.md">العربية</a>
</p>

<h1 align="center">DocMind AI</h1>

<p align="center">
  <strong>Multilingual AI Document Assistant powered by Retrieval-Augmented Generation (RAG)</strong>
</p>

<p align="center">
  Upload documents, ask questions in Arabic or English, and receive document-grounded answers with source references.
</p>

<p align="center">
  <a href="https://docmind-ai-smoky.vercel.app"><strong>Live Demo</strong></a> ·
  <a href="https://docmind-ai-api-k5f4.onrender.com/docs"><strong>API Docs</strong></a> ·
  <a href="README_AR.md"><strong>Arabic README</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-Frontend-black?logo=nextdotjs" alt="Next.js" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-Backend-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-Frontend-3178C6?logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Google%20Gemini-AI-8E75B2?logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/Vercel-Frontend-black?logo=vercel" alt="Vercel" />
  <img src="https://img.shields.io/badge/Render-Backend-46E3B7?logo=render&logoColor=black" alt="Render" />
</p>

---

## Overview

**DocMind AI** is a full-stack multilingual document intelligence application designed to help users understand large collections of files without manually reading every page.

Instead of behaving like a general-purpose chatbot, DocMind uses a **Retrieval-Augmented Generation (RAG)** pipeline. Uploaded documents are parsed, split into searchable chunks, converted into semantic embeddings, ranked against the user's question, and then passed to a language model as grounded context.

The system is designed to answer from the selected uploaded documents, show the supporting source, and state when the requested information is not found in the retrieved context.

The public version supports **Arabic and English**, including cross-language retrieval such as asking an Arabic question about an English document.

---

## Live Application

| Component | URL | Status |
| --- | --- | --- |
| Web App | https://docmind-ai-smoky.vercel.app | Online |
| Backend API | https://docmind-ai-api-k5f4.onrender.com | Online |
| Swagger API Docs | https://docmind-ai-api-k5f4.onrender.com/docs | Online |

> The backend currently uses Render's free web-service tier. After inactivity, the first request can be slower while the service wakes up.

---

## Main Features

| Feature | Description |
| --- | --- |
| **Multiple document upload** | Upload and process one or multiple files in the same session. |
| **PDF support** | Extracts readable text and keeps page-level references. |
| **DOCX support** | Extracts paragraphs from Microsoft Word documents. |
| **PPTX support** | Extracts text from PowerPoint slides and keeps slide references. |
| **Arabic & English interface** | The user interface can switch between Arabic and English. |
| **Cross-language Q&A** | Ask in Arabic about English documents, or in English about Arabic content. |
| **Semantic retrieval** | Uses multilingual embeddings instead of relying only on exact keyword matches. |
| **RAG architecture** | Retrieves relevant document chunks before generating an answer. |
| **Grounded prompting** | The answer model is explicitly instructed to use the retrieved document context and avoid unsupported guesses. |
| **Source citations** | Answers can reference supporting sources using `[1]`, `[2]`, and similar markers. |
| **Source location** | Displays the file name and page, paragraph, or slide where relevant content was found. |
| **Similarity scoring** | Retrieval results include semantic similarity values. |
| **Intent boosting** | Adds a lightweight relevance boost for structured fields such as name, university, phone, email, skills, and experience. |
| **Document-scoped questions** | The API restricts retrieval to the selected document IDs supplied by the current client. |
| **Summarization endpoint** | The backend includes `/summarize` for document-grounded summaries. |
| **Interactive API documentation** | FastAPI exposes Swagger documentation at `/docs`. |
| **Responsive web UI** | Designed to work on desktop and mobile browsers. |
| **Cloud-hosted AI** | Visitors can use the public demo without installing Python, Ollama, or a local model. |

---

## How It Works

```text
PDF / DOCX / PPTX
        │
        ▼
  Text Extraction
        │
        ▼
Chunking + Source Metadata
(file + page/slide/paragraph)
        │
        ▼
 Gemini Embedding 2
        │
        ▼
 In-Memory Vector Store
        │
        ▼
    User Question
        │
        ▼
 Query Embedding
        │
        ▼
Cosine Similarity + Intent Boost
        │
        ▼
 Top Relevant Chunks
        │
        ▼
 Gemini 3.8 Flash
        │
        ▼
Grounded Answer + Sources
```

### 1. Document ingestion

The FastAPI backend accepts:

- `.pdf`
- `.docx`
- `.pptx`

Document parsing uses:

- **PyPDF** for PDF files
- **python-docx** for Word documents
- **python-pptx** for PowerPoint presentations

### 2. Source-aware extraction

DocMind preserves location metadata during extraction:

- PDF → `Page X`
- DOCX → `Paragraph X`
- PPTX → `Slide X`

That metadata follows each chunk through retrieval so the user can see where the answer came from.

### 3. Chunking

Long content is split into overlapping chunks. The chunking logic attempts to break text near natural boundaries such as line breaks and Arabic/English sentence punctuation.

### 4. Embeddings

Each chunk is converted into a semantic vector using **Gemini Embedding 2** (`gemini-embedding-2`). The current implementation requests **768-dimensional embeddings**.

### 5. Retrieval

When a question is submitted:

1. an embedding is generated for the question;
2. cosine similarity is calculated against stored chunks;
3. a lightweight field-intent boost can improve common structured queries;
4. results are ranked;
5. only the top relevant chunks are provided to the answer model.

### 6. Answer generation

The retrieved context is sent to **Gemini 3.8 Flash** (`gemini-3.8-flash`).

The system instructions require the model to:

- use the supplied document context;
- avoid guessing missing facts;
- preserve exact names, emails, phone numbers, identifiers, and dates;
- answer in the same language as the user's question by default;
- cite supporting sources;
- state when requested information is not found.

---

## Multilingual Example

A document can contain:

```text
University: King Abdulaziz University
```

The user can ask:

```text
ما هي الجامعة؟
```

DocMind can retrieve the English content semantically and answer in Arabic while keeping the original factual value.

The reverse direction also works: an English question can retrieve relevant Arabic content.

---

## Source-Aware Answers

Example:

```text
Question:
What university did Ziyad attend?

Answer:
Ziyad attended King Abdulaziz University. [1]

Source [1]:
File: (CV) ZIYAD Alghamdi.pdf
Location: Page 1
```

The interface also displays a preview of retrieved source text so users can compare the generated answer with the original context.

---

## Tech Stack

### Frontend

| Technology | Purpose |
| --- | --- |
| **Next.js** | Web application framework |
| **React** | UI and client-side state |
| **TypeScript** | Type-safe frontend development |
| **Tailwind CSS** | Responsive styling |
| **Vercel** | Frontend hosting and deployment |

### Backend

| Technology | Purpose |
| --- | --- |
| **Python** | Backend and document processing |
| **FastAPI** | REST API |
| **Uvicorn** | ASGI server |
| **HTTPX** | Gemini API requests |
| **NumPy** | Vector operations and cosine similarity |
| **PyPDF** | PDF text extraction |
| **python-docx** | DOCX extraction |
| **python-pptx** | PPTX extraction |
| **Render** | Backend hosting |

### AI & Retrieval

| Technology | Purpose |
| --- | --- |
| **Gemini 3.8 Flash** | Answer generation and summarization |
| **Gemini Embedding 2** | Multilingual semantic embeddings |
| **RAG** | Grounds responses in retrieved document context |
| **Cosine Similarity** | Ranks chunks by semantic relevance |
| **Intent Boosting** | Improves selected structured-field searches |

---

## System Architecture

```text
┌──────────────────────────┐
│      User / Browser      │
│    Desktop or Mobile     │
└─────────────┬────────────┘
              │ HTTPS
              ▼
┌──────────────────────────┐
│     Next.js Frontend     │
│          Vercel          │
└─────────────┬────────────┘
              │ REST API
              ▼
┌──────────────────────────┐
│     FastAPI Backend      │
│          Render          │
├──────────────────────────┤
│ Document Extraction      │
│ Chunking                 │
│ Embedding Storage        │
│ Semantic Retrieval       │
│ Citation Mapping         │
└─────────────┬────────────┘
              │ Gemini API
              ▼
┌──────────────────────────┐
│      Google Gemini       │
│  gemini-embedding-2      │
│  gemini-3.8-flash        │
└──────────────────────────┘
```

---

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | API information |
| `GET` | `/health` | Service and AI configuration health check |
| `POST` | `/upload` | Extract, chunk, and embed uploaded files |
| `POST` | `/search` | Retrieve semantically relevant chunks |
| `POST` | `/ask` | Answer using retrieved document context |
| `POST` | `/summarize` | Generate a document-grounded summary |

Interactive documentation:

**https://docmind-ai-api-k5f4.onrender.com/docs**

---

## Project Structure

```text
DocMind-AI/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── .gitignore
├── render.yaml
├── README.md
└── README_AR.md
```

---

## Deployment

### Frontend — Vercel

The production frontend is hosted on Vercel.

```env
NEXT_PUBLIC_API_URL=https://docmind-ai-api-k5f4.onrender.com
```

### Backend — Render

The FastAPI backend is hosted as a Render Web Service.

Required secret:

```env
GEMINI_API_KEY=your_gemini_api_key
```

CORS is configured with an allowed-origin environment variable such as:

```env
ALLOWED_ORIGINS=https://docmind-ai-smoky.vercel.app
```

The Gemini API key is stored on the backend and is not included in the browser bundle or committed to GitHub.

---

## Run Locally

### Prerequisites

- Git
- Node.js
- Python
- Gemini API key

### 1. Clone

```bash
git clone https://github.com/ziyad-alghamdi/DocMind-AI.git
cd DocMind-AI
```

### 2. Backend

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the environment variables.

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
$env:ALLOWED_ORIGINS="http://localhost:3000"
```

macOS / Linux:

```bash
export GEMINI_API_KEY="YOUR_KEY"
export ALLOWED_ORIGINS="http://localhost:3000"
```

Start the backend:

```bash
uvicorn main:app --reload
```

API: `http://localhost:8000`

Swagger: `http://localhost:8000/docs`

### 3. Frontend

In another terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run:

```bash
npm run dev
```

Open `http://localhost:3000`.

---

## Download the Project

Download the source from GitHub using **Code → Download ZIP**, or clone it:

```bash
git clone https://github.com/ziyad-alghamdi/DocMind-AI.git
```

---

## Security & Privacy Notes

- The Gemini API key is stored as a backend environment variable.
- API keys and `.env` files are excluded from GitHub.
- Local Python virtual environments and generated build folders are ignored.
- Uploaded document text is processed by the backend; relevant content is sent to the Gemini API to create embeddings and generate answers.
- The current prototype stores processed documents and embeddings **in server memory**, not in a persistent database.
- In-memory data is lost when the Render service restarts or redeploys.
- The public prototype currently has no user authentication or persistent personal document storage.

---

## Current Prototype Limitations

This repository is a working portfolio prototype, not a full production document-management platform.

Current limitations include:

- scanned image-only PDFs do not yet have OCR support;
- maximum upload size is currently **10 MB per file**;
- processed documents and embeddings are stored in memory;
- no persistent vector database is connected yet;
- no user accounts or persistent chat history;
- Render's free tier can make the first request slower after inactivity;
- the backend includes summarization, while the public UI currently focuses mainly on upload and document Q&A.

---

## Roadmap

- OCR for scanned PDFs and images
- Persistent vector database
- User authentication
- Private document workspaces
- Persistent conversation history
- Document deletion and lifecycle controls
- Streaming responses
- Stronger reranking
- Background ingestion jobs
- Upload progress indicators
- More file formats
- Automated RAG quality evaluation
- Rate limiting and stronger production access controls
- Custom domain
- Automated tests and CI/CD quality checks

---

## What This Project Demonstrates

DocMind AI demonstrates practical implementation of:

- Full-stack AI development
- Retrieval-Augmented Generation
- Semantic vector search
- Multilingual embeddings
- Prompt grounding and anti-hallucination constraints
- Source attribution
- Document parsing
- REST API design
- Frontend/backend integration
- Secret management
- Cloud deployment with Vercel and Render

---

## Developer

**Ziyad Alghamdi**

- GitHub: https://github.com/ziyad-alghamdi
- LinkedIn: https://www.linkedin.com/in/ziyad-alghamdi-a97366251
- Repository: https://github.com/ziyad-alghamdi/DocMind-AI
- Live Demo: https://docmind-ai-smoky.vercel.app

---

## Copyright

© 2026 Ziyad Alghamdi. All rights reserved.

The repository is publicly viewable and downloadable from GitHub. No separate open-source license is granted unless a license file is added to the repository.