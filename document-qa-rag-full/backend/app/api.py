from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .ingestion import save_upload, extract_text_from_file
from .chunker import semantic_chunk_paragraphs
from .embeddings import embed_texts, generate_answer
from .vector_db import upsert_chunks
from .retriever import retrieve
from .memory import add_to_session, get_session_context
from .feedback import store_feedback
import uuid
from pathlib import Path

router = APIRouter()

@router.post('/api/upload')
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    fname = f"{uuid.uuid4().hex}_{file.filename}"
    path = save_upload(content, fname)
    text = extract_text_from_file(path)
    chunks = semantic_chunk_paragraphs(text)
    metadatas = [{"source": fname, "page": None, "chunk_index": i} for i in range(len(chunks))]
    embeddings = embed_texts(chunks)
    upsert_chunks(fname, chunks, embeddings, metadatas)
    return {"status": "ok", "doc_id": fname, "chunks": len(chunks)}

@router.post('/qa')
async def qa(query: dict):
    session_id = query.get('session_id', 'anonymous')
    q = query.get('query')
    if not q:
        raise HTTPException(status_code=400, detail="query required")
    # retrieve top chunks
    res = retrieve(q, top_k=5)
    context_texts = res.get('documents', [[]])[0]
    # build prompt using retrieved context and short-term memory
    history = get_session_context(session_id)
    prompt_parts = ["You are a helpful assistant. Use the context below to answer the question."]
    for i, (qq, aa) in enumerate(history):
        prompt_parts.append(f"Previous Q: {qq}\nPrevious A: {aa}\n")
    prompt_parts.append("Context:\n" + "\n---\n".join(context_texts))
    prompt_parts.append("User question:\n" + q)
    prompt = "\n\n".join(prompt_parts)
    answer = generate_answer(prompt)
    add_to_session(session_id, q, answer)
    return JSONResponse({"answer": answer, "retrieved": context_texts})

@router.post('/feedback')
async def feedback(entry: dict):
    store_feedback(entry)
    return {"status": "ok"}
