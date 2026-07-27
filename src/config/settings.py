
import http

from dotenv import load_dotenv
import os

load_dotenv()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"

CHROMA_DIR = BASE_DIR / "storage" / "chroma"

REPORT_DIR = BASE_DIR / "output" / "reports"

SCREENSHOT_DIR = BASE_DIR / "screenshots"


# BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")

BASE_URL = os.getenv("BASE_URL", "http://host.docker.internal:11434")

 


LLM_MODEL = "llama3.2"

EMBEDDING_MODEL = "nomic-embed-text"

CHUNK_SIZE = 800

CHUNK_OVERLAP = 100

TOP_K_RESULTS = 5

EMBED_BATCH_SIZE = 100


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")



# MODEL = os.getenv("MODEL", "llama3.2")
# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")


# CHROMA_PATH = os.getenv("CHROMA_PATH", "storage/chroma")

# DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "documents")


# EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "100"))


# TOP_K = int(os.getenv("TOP_K", 5))