from .embeddings import embed_texts
from .vector_db import query_embeddings

def retrieve(query: str, top_k: int = 5):
    q_emb = embed_texts([query])[0]
    res = query_embeddings(q_emb, top_k=top_k)
    return res
