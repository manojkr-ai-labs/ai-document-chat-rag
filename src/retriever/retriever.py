from src.vectorstore.chroma_store import vector_db
from src.config import TOP_K
from src.utils.logger import logger
 
def retrieve_context(query: str):
    """
    Search the vector database and return the most relevant chunks.
    """

    logger.info("=" * 60)
    logger.info("Searching Vector Database...")
    logger.info("=" * 60)   
    results = vector_db.similarity_search_with_score(
        query=query,
        k=TOP_K
    )

    logger.info(f"Retrieved {len(results)} chunks")

    return results