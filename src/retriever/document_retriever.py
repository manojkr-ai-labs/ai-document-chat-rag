from src.vectorstore.chroma_store import vector_db
from src.config.settings import (
    RELEVANCE_THRESHOLD,
    TOP_K_RESULTS,
)
from src.utils.logger import logger
from src.retriever.retrieval_result import RetrievalResult


def retrieve_documents(
    query: str,
    k: int = TOP_K_RESULTS,
    threshold: float = RELEVANCE_THRESHOLD,
):
    logger.info("========== RETRIEVER START ==========")
    logger.info("Retrieval request received")
    logger.info(
        f"Retrieval config | top_k={k} "
        f"| threshold={threshold}"
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

        if score < threshold:
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


def retrieve_candidates(
    query: str,
    k: int = TOP_K_RESULTS,
) -> list[RetrievalResult]:
    logger.info(
        "========== CANDIDATE RETRIEVAL START =========="
    )
    logger.info("Candidate retrieval request received")
    logger.info(
        f"Candidate retrieval config | top_k={k}"
    )

    results = vector_db.similarity_search_with_score(
        query=query,
        k=k,
    )

    candidates = [
        RetrievalResult(
            document=document,
            retrieval_score=score,
        )
        for document, score in results
    ]

    logger.info(
        f"Retrieved {len(candidates)} candidates"
    )

    logger.info(
        "========== CANDIDATE RETRIEVAL END =========="
    )

    return candidates