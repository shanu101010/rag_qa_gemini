import os

DATA_DIR = os.environ.get("DATA_DIR", "./data")
CHROMA_DIR = os.environ.get("CHROMA_DIR", "./chroma_db")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GOOGLE_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
USE_VERTEX_AI = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() in ("1","true","yes")
MAX_CHUNK_TOKENS = int(os.environ.get("MAX_CHUNK_TOKENS", "512"))
OVERLAP_TOKENS = int(os.environ.get("OVERLAP_TOKENS", "128"))
SHORT_TERM_WINDOW = int(os.environ.get("SHORT_TERM_WINDOW", "20"))

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
