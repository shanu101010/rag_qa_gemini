from typing import List
from .config import MAX_CHUNK_TOKENS, OVERLAP_TOKENS

def naive_tokenize(text: str):
    return text.split()

def chunk_text(text: str, chunk_size_tokens=MAX_CHUNK_TOKENS, overlap_tokens=OVERLAP_TOKENS):
    words = naive_tokenize(text)
    chunks = []
    i = 0
    n = len(words)
    while i < n:
        j = min(i + chunk_size_tokens, n)
        chunk_words = words[i:j]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
        i = j - overlap_tokens
        if i <= 0:
            i = j
    return chunks

def semantic_chunk_paragraphs(text: str):
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    out = []
    for p in paras:
        if len(p.split()) > MAX_CHUNK_TOKENS:
            out.extend(chunk_text(p))
        else:
            out.append(p)
    return out
