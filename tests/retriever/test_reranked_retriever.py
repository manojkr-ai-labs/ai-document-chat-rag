from src.retriever.reranked_retriever import RerankedRetriever


def test_reranked_retriever_returns_relevant_documents():
    retriever = RerankedRetriever()

    results = retriever.retrieve(
        "What is IATA Annual?",
        k=5,
        top_n=2,
    )

    assert results

    for result in results:
        assert result.document is not None
        assert result.rerank_score is not None
        assert result.rerank_score >= 0.005