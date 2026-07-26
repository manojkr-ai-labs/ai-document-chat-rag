from src.vectorstore.chroma_store import vector_db
from src.config.settings import TOP_K_RESULTS


def retrieve_documents(query: str, k: int = TOP_K_RESULTS):
    """
    Retrieve the most relevant chunks from ChromaDB.
    """

    results = vector_db.similarity_search(
        query=query,
        k=k
    )

    return results