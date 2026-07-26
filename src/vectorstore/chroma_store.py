from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

from src.config.settings import CHROMA_DIR
 

embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_db = Chroma(
    collection_name="ndsap",
    embedding_function=embedding, 
    persist_directory=str(CHROMA_DIR)
)