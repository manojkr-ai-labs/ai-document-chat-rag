from langchain_ollama import ChatOllama 
from src.config.settings import LLM_MODEL, BASE_URL

llm = ChatOllama(
    model=LLM_MODEL,
    base_url=BASE_URL,
    temperature=0,
)