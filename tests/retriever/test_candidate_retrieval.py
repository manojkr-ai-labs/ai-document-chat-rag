from src.retriever.document_retriever import retrieve_candidates


def test_retrieve_candidates():
    candidates = retrieve_candidates(
        "What is IATA Annual?",
        k=5,
    )

    assert len(candidates) == 5

    for candidate in candidates:
        assert candidate.document is not None
        assert isinstance(candidate.retrieval_score, float)
        assert candidate.rerank_score is None