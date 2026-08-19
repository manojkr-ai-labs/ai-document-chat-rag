from tests.evaluation.retrieval_questions import EVALUATION_QUESTIONS
from src.retriever.reranked_retriever import RerankedRetriever


retriever = RerankedRetriever()


def test_reranked_retrieval_returns_expected_sources():
    for case in EVALUATION_QUESTIONS:
        if not case["should_retrieve"]:
            continue

        results = retriever.retrieve(
            query=case["question"],
        )

        sources = {
            result.document.metadata.get("source", "")
            for result in results
        }

        assert any(
            case["expected_source"] in source
            for source in sources
        ), (
            f"Expected source not retrieved for: "
            f"{case['question']}"
        )

        assert all(
            result.rerank_score is not None
            for result in results
        ), (
            f"Missing rerank score for: "
            f"{case['question']}"
        )


def test_reranked_retrieval_rejects_irrelevant_queries():
    for case in EVALUATION_QUESTIONS:
        if case["should_retrieve"]:
            continue

        results = retriever.retrieve(
            query=case["question"],
        )

        assert results == [], (
            f"Unexpected documents retrieved for: "
            f"{case['question']}"
        )