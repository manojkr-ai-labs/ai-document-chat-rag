from src.retriever.query_expander import expand_query
from src.reranker.cross_encoder_reranker import CrossEncoderReranker
from src.retriever.document_retriever import retrieve_candidates


def test_query_expansion_improves_iata_reranking():

    original_query = "What is IATA Annual?"

    expanded_query = expand_query(
        original_query
    )

    reranker = CrossEncoderReranker()

    candidates = retrieve_candidates(
        query=original_query,
        k=5,
    )

    original_results = reranker.rerank(
        query=original_query,
        candidates=candidates,
        top_n=5,
    )

    expanded_results = reranker.rerank(
        query=expanded_query,
        candidates=candidates,
        top_n=5,
    )

    original_score = original_results[0].rerank_score
    expanded_score = expanded_results[0].rerank_score

    print("\n" + "=" * 80)
    print("QUERY EXPANSION EXPERIMENT")
    print("=" * 80)

    print(
        f"Original query:  {original_query}"
    )

    print(
        f"Expanded query:  {expanded_query}"
    )

    print(
        f"Original score:  {original_score}"
    )

    print(
        f"Expanded score:  {expanded_score}"
    )

    assert expanded_score > original_score