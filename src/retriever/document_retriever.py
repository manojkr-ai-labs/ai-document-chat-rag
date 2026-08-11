from src.vectorstore.chroma_store import vector_db
from src.config.settings import TOP_K_RESULTS
from src.utils.logger import logger


def retrieve_documents(
    query: str,
    k: int = TOP_K_RESULTS,
):
    logger.info("========== RETRIEVER START ==========")
    logger.info(f"Query: {query}")

    results = vector_db.similarity_search_with_score(
        query=query,
        k=k,
    )

    logger.info(
        f"Chroma returned {len(results)} documents"
    )

    relevant_documents = []

    for document, score in results:
        logger.info(
            f"Retrieved | score={score:.4f} "
            f"| source={document.metadata.get('source')} "
            f"| page={document.metadata.get('page')}"
        )

        relevant_documents.append(document)

    logger.info(
        f"Relevant documents: "
        f"{len(relevant_documents)}/{len(results)}"
    )

    logger.info("========== RETRIEVER END ==========")

    return relevant_documents