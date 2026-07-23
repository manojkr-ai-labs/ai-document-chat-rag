from dotenv import load_dotenv
import os

load_dotenv()

MODEL = os.getenv("MODEL", "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")

CHROMA_PATH = os.getenv("CHROMA_PATH", "storage/chroma")
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "documents")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "100"))
