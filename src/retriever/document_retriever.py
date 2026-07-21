from src.vectorstore.chroma_store import vector_db


def retrieve_documents(query: str, k: int = 5):
    """
    Retrieve the most relevant chunks from ChromaDB.
    """

    results = vector_db.similarity_search(
        query=query,
        k=k
    )

    return results