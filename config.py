import os

from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

CHROMA_DB_HOST = os.getenv("CHROMA_DB_HOST")

CHROMA_DB_PORT = int(os.getenv("CHROMA_DB_PORT"))

RAG_DATA_DIR = os.getenv("RAG_DATA_DIR")

CHUNK_LENGTH = int(os.getenv("CHUNK_LENGTH"))

SERVER_PORT = int(os.getenv("SERVER_PORT"))

UPLOAD_DIR = "uploads"

os.makedirs(RAG_DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
