from pathlib import Path
from .config import DATA_DIR
from pdfminer.high_level import extract_text as extract_pdf_text

def save_upload(file_bytes: bytes, filename: str) -> str:
    path = Path(DATA_DIR) / filename
    with open(path, "wb") as f:
        f.write(file_bytes)
    return str(path)

def extract_text_from_file(path: str) -> str:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf_text(path)
    elif suffix in {".docx", ".doc"}:
        import docx
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif suffix in {".txt", ".md", ".html"}:
        return open(path, "r", encoding="utf-8", errors="ignore").read()
    else:
        # fallback - requires textract system deps on some platforms
        try:
            import textract
            return textract.process(path).decode("utf-8", errors="ignore")
        except Exception:
            return open(path, "rb").read().decode("utf-8", errors="ignore")
