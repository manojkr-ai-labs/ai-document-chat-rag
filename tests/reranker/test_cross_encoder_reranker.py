from src.retriever.document_retriever import retrieve_candidates
from src.reranker.cross_encoder_reranker import CrossEncoderReranker


def test_cross_encoder_reranker():
    query = "What is IATA Annual?"

    candidates = retrieve_candidates(
        query,
        k=5,
    )

    reranker = CrossEncoderReranker()

    
    ranked = reranker.rerank(
    query,
    candidates,
    top_n=2,
)

    assert len(ranked) == 2
 

    for result in ranked:
        assert result.document is not None
        assert isinstance(result.retrieval_score, float)
        assert isinstance(result.rerank_score, float)