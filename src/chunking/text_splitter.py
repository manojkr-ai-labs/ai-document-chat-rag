from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


def split_documents(documents):
    """
    Split LangChain Documents while preserving metadata.
    """
    return text_splitter.split_documents(documents)