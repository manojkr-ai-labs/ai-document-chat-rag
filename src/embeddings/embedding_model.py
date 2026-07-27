from langchain_ollama import OllamaEmbeddings
from src.config.settings import BASE_URL, EMBEDDING_MODEL

embedding_model = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=BASE_URL,
)