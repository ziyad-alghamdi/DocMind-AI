# DocMind AI Frontend

This directory contains the **Next.js frontend** for DocMind AI.

The interface allows users to:

- upload PDF, DOCX, and PPTX documents;
- switch between Arabic and English;
- submit questions about uploaded documents;
- receive document-grounded answers;
- review the source file and source location used to support an answer;
- use the application from desktop or mobile browsers.

## Stack

- Next.js
- React
- TypeScript
- Tailwind CSS
- Vercel

## Backend Connection

The frontend reads the backend URL from:

```env
NEXT_PUBLIC_API_URL
```

For local development:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

The public production frontend currently connects to the FastAPI backend hosted on Render.

## Run Locally

```bash
npm install
npm run dev
```

Then open:

```text
http://localhost:3000
```

## Production

Live application:

https://docmind-ai-smoky.vercel.app

Main project documentation:

- English: `../README.md`
- العربية: `../README_AR.md`

## Developer

**Ziyad Alghamdi**

- GitHub: https://github.com/ziyad-alghamdi
- LinkedIn: https://www.linkedin.com/in/ziyad-alghamdi-a97366251
