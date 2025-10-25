from chromadb import Client
from chromadb.config import Settings
from .config import CHROMA_DIR
from pathlib import Path

client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))

COL_NAME = "documents"
if COL_NAME not in [c.name for c in client.list_collections()]:
    collection = client.create_collection(name=COL_NAME)
else:
    collection = client.get_collection(COL_NAME)

def upsert_chunks(doc_id: str, chunks: list, embeddings: list, metadatas: list):
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    collection.add(ids=ids, documents=chunks, metadatas=metadatas, embeddings=embeddings)
    client.persist()

def query_embeddings(query_emb, top_k=5):
    res = collection.query(query_embeddings=[query_emb], n_results=top_k)
    return res
