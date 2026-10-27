<p align="center">
  <strong>English</strong> | <a href="README_AR.md">العربية</a>
</p>

# DocMind AI

DocMind AI is a multilingual AI-powered document assistant that helps users understand large amounts of information without reading every file manually.

Users can upload documents, ask questions in Arabic or English, and receive answers based only on the content of their uploaded files. DocMind also shows the source file and page used to support each answer.

## Features

- Upload multiple documents
- Supports PDF, DOCX, and PPTX
- Ask questions in Arabic or English
- Ask Arabic questions about English documents
- Semantic search using embeddings
- Retrieval-Augmented Generation (RAG)
- Answers grounded in uploaded documents
- Source file and page references
- Arabic and English user interface
- Local AI processing using Ollama
- No paid AI API required for local use

## How It Works

```text
Documents
   ↓
Text Extraction
   ↓
Text Chunking
   ↓
Embeddings
   ↓
Semantic Search
   ↓
Relevant Context
   ↓
Local LLM
   ↓
Answer + Source
```

DocMind extracts text from uploaded files and divides the content into smaller chunks. The chunks are converted into embeddings and stored temporarily in memory.

When the user asks a question, DocMind performs semantic search to find the most relevant sections of the uploaded documents. The retrieved context is then provided to the language model, which generates an answer using only the document content.

## AI Models

DocMind currently uses local models through Ollama:

- **BGE-M3** — multilingual embeddings and semantic search
- **Qwen3 8B** — question answering and document understanding

This allows DocMind to run locally without requiring a paid AI API.

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI

### AI

- Ollama
- Qwen3
- BGE-M3
- Retrieval-Augmented Generation (RAG)

### Document Processing

- PyPDF
- python-docx
- python-pptx

## Arabic & English Support

DocMind supports multilingual interaction. For example, a document can be written in English:

```text
University: King Abdulaziz University
```

The user can ask:

```text
ما هي الجامعة؟
```

DocMind can answer in Arabic while retrieving the information from the English document.

## Source-Aware Answers

DocMind displays the document source used for the answer.

Example:

```text
Question:
What university did Ziyad attend?

Answer:
Ziyad attended King Abdulaziz University. [1]

Source:
(CV) ZIYAD Alghamdi.pdf
Page 1
```

If the requested information is not available in the uploaded documents, DocMind is designed to state that the information was not found instead of relying on outside knowledge.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ziyad-alghamdi/DocMind-AI.git
cd DocMind-AI
```

### 2. Install Ollama

Download Ollama from:

https://ollama.com

Then install the required models:

```bash
ollama pull bge-m3
ollama pull qwen3:8b
```

### 3. Backend

Open the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install fastapi uvicorn python-multipart pypdf python-docx python-pptx numpy httpx
```

Run the backend:

```bash
fastapi dev main.py
```

Backend:

```text
http://localhost:8000
```

### 4. Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

## Project Structure

```text
DocMind-AI/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── app/
│   ├── public/
│   └── package.json
│
└── .gitignore
```

## Future Improvements

- Cloud deployment
- User accounts
- Persistent document storage
- Vector database integration
- Conversation history
- Improved hallucination prevention
- OCR support for scanned PDFs
- More document formats
- Faster document processing
- Document-level selection before asking questions

## Developer

**Ziyad Alghamdi**

- GitHub: https://github.com/ziyad-alghamdi
- LinkedIn: https://www.linkedin.com/in/ziyad-alghamdi-a97366251

## Copyright

© 2026 Ziyad Alghamdi. All rights reserved.

This project was developed for educational and portfolio purposes.
