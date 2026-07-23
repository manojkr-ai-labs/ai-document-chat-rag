from langchain_ollama import ChatOllama
from src.config import MODEL, BASE_URL

llm = ChatOllama(
    model=MODEL,
    base_url=BASE_URL,
    temperature=0,
)