from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

from src.config.settings import (
    CHROMA_DIR,
    BASE_URL,
    EMBEDDING_MODEL,
)

embedding = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=BASE_URL,
)

vector_db = Chroma(
    collection_name="ndsap",
    embedding_function=embedding,
    persist_directory=str(CHROMA_DIR),
)