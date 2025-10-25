import os
from typing import List
from .config import GEMINI_API_KEY, USE_VERTEX_AI, GOOGLE_PROJECT, GOOGLE_LOCATION
# google-genai SDK
try:
    from google import genai
    from google.genai import types as genai_types
except Exception:
    genai = None
    genai_types = None

def make_client():
    if genai is None:
        raise RuntimeError("google-genai SDK not installed. Install with: pip install google-genai")
    if USE_VERTEX_AI:
        client = genai.Client(vertexai=True, project=GOOGLE_PROJECT, location=GOOGLE_LOCATION)
    else:
        # Gemini Developer API via API key
        client = genai.Client(api_key=GEMINI_API_KEY)
    return client

def embed_texts(texts: List[str], model: str = "gemini-embedding-001") -> List[List[float]]:
    """Return embeddings for a list of texts using Gemini embedding model."""
    client = make_client()
    # embed_content expects contents to be list of strings
    response = client.models.embed_content(model=model, contents=texts)
    # response.embeddings is a list of ContentEmbedding objects; extract .values
    embeddings = []
    for emb in response.embeddings:
        # each emb may have .values or .values property
        vals = getattr(emb, 'values', None) or getattr(emb, 'vector', None) or list(emb)
        embeddings.append(list(vals))
    return embeddings

def generate_answer(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """Generate text answer using Gemini model."""
    client = make_client()
    # simple generation example
    response = client.models.generate_content(model=model, contents=prompt)
    # response may have .text or .output[0].content etc. we handle common cases
    out = getattr(response, 'text', None)
    if out:
        return out
    # try parts
    try:
        # response.output is list of parts with 'content' (for some SDK versions)
        parts = getattr(response, 'output', None)
        if parts:
            texts = []
            for p in parts:
                txt = getattr(p, 'content', None) or getattr(p, 'text', None)
                if txt:
                    texts.append(txt)
            return "\n".join(texts)
    except Exception:
        pass
    # fallback to str(response)
    return str(response)
