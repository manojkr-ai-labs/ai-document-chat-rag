from src.vectorstore.chroma_store import vector_db
from src.config.settings import (
    RELEVANCE_THRESHOLD,
    TOP_K_RESULTS,
)
from src.utils.logger import logger


def retrieve_documents(
    query: str,
    k: int = TOP_K_RESULTS,
):
    logger.info("========== RETRIEVER START ==========")
    logger.info(f"Query: {query}")
    logger.info(
        f"Retrieval config | top_k={k} "
        f"| threshold={RELEVANCE_THRESHOLD}"
    )

    results = vector_db.similarity_search_with_score(
        query=query,
        k=k,
    )

    logger.info(
        f"Chroma returned {len(results)} documents"
    )

    relevant_documents = []

    for document, score in results:
        source = document.metadata.get(
            "source",
            "Unknown",
        )
        page = document.metadata.get(
            "page",
            "?",
        )

        if score < RELEVANCE_THRESHOLD:
            relevant_documents.append(document)

            logger.info(
                f"ACCEPTED | score={score:.4f} "
                f"| source={source} "
                f"| page={page}"
            )
        else:
            logger.info(
                f"REJECTED | score={score:.4f} "
                f"| source={source} "
                f"| page={page}"
            )

    logger.info(
        f"Relevant documents: "
        f"{len(relevant_documents)}/{len(results)}"
    )

    logger.info("========== RETRIEVER END ==========")

    return relevant_documents