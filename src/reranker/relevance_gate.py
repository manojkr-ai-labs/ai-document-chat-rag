from src.config.settings import RERANK_RELEVANCE_THRESHOLD
from src.retriever.retrieval_result import RetrievalResult


def filter_relevant_results(
    results: list[RetrievalResult],
    threshold: float = RERANK_RELEVANCE_THRESHOLD,
) -> list[RetrievalResult]:
    return [
        result
        for result in results
        if (
            result.rerank_score is not None
            and result.rerank_score >= threshold
        )
    ]