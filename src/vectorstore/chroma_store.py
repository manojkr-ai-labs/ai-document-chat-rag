from langchain_chroma import Chroma

from src.embeddings.embedding_model import embedding_model
from src.config.settings import CHROMA_DIR

vector_db = Chroma(
    collection_name="ndsap",
    embedding_function=embedding_model,
    persist_directory=str(CHROMA_DIR),
)