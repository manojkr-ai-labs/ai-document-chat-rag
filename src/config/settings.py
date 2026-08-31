import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"

CHROMA_DIR = Path(
    os.getenv("CHROMA_DIR", str(BASE_DIR / "storage" / "chroma"))
)

REPORT_DIR = BASE_DIR / "output" / "reports"

SCREENSHOT_DIR = BASE_DIR / "screenshots"

BASE_URL = os.getenv(
    "BASE_URL",
    "http://host.docker.internal:11434",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama3.2:latest",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text:latest",
)
RERANKER_MODEL = os.getenv(
    "RERANKER_MODEL",
    "BAAI/bge-reranker-base",
)

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

TOP_K_RESULTS = 5

RELEVANCE_THRESHOLD = float(
    os.getenv("RELEVANCE_THRESHOLD", "1.0")
)

RERANK_TOP_N = 2
RERANK_RELEVANCE_THRESHOLD = 0.005

EMBED_BATCH_SIZE = int(
    os.getenv("EMBED_BATCH_SIZE", "100")
)
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)