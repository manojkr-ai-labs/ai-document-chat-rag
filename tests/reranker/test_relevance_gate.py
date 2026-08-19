from langchain_core.documents import Document

from src.config.settings import RERANK_RELEVANCE_THRESHOLD
from src.retriever.retrieval_result import RetrievalResult
from src.reranker.relevance_gate import filter_relevant_results


def make_result(score: float | None) -> RetrievalResult:
    return RetrievalResult(
        document=Document(page_content="test"),
        retrieval_score=1.0,
        rerank_score=score,
    )


def test_relevance_gate_accepts_score_above_threshold():
    results = [
        make_result(RERANK_RELEVANCE_THRESHOLD + 0.001),
    ]

    filtered = filter_relevant_results(results)

    assert len(filtered) == 1


def test_relevance_gate_accepts_score_equal_to_threshold():
    results = [
        make_result(RERANK_RELEVANCE_THRESHOLD),
    ]

    filtered = filter_relevant_results(results)

    assert len(filtered) == 1


def test_relevance_gate_rejects_score_below_threshold():
    results = [
        make_result(RERANK_RELEVANCE_THRESHOLD - 0.001),
    ]

    filtered = filter_relevant_results(results)

    assert len(filtered) == 0


def test_relevance_gate_rejects_missing_score():
    results = [
        make_result(None),
    ]

    filtered = filter_relevant_results(results)

    assert len(filtered) == 0