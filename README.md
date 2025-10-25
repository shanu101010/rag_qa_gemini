# Document-QA-RAG (Full Project)

This repository contains a demo production scaffold for a Retrieval-Augmented Generation (RAG) Document Q&A system
with memory support using **Google Gemini** for embeddings and generation, **ChromaDB** for vector storage,
a **FastAPI** backend, and a **React + Vite** frontend.

## Quickstart (local demo)
1. Backend:
   - Go to `backend/`.
   - Create a Python 3.10+ venv and `pip install -r requirements.txt`.
   - Set environment variables:
     - `GEMINI_API_KEY` (for Gemini Developer API) **or** set `GOOGLE_GENAI_USE_VERTEXAI=true` and configure Google Cloud env vars.
   - Run: `uvicorn app.main:app --reload --port 8000`

2. Frontend:
   - Go to `frontend/`.
   - `npm install`
   - `npm run dev`
   - Open the Vite dev URL (usually http://localhost:5173)

## Notes
- The backend uses the `google-genai` Python SDK to call Gemini embedding and generation models.
- Replace environment variables with your API key or Vertex AI configuration.
- This demo stores uploaded files and Chroma DB data locally in the backend folder.

## Files included
- `backend/` — FastAPI app with ingestion, chunking, embeddings (Gemini), vector DB (Chroma), memory and feedback endpoints.
- `frontend/` — React + Vite demo app.

