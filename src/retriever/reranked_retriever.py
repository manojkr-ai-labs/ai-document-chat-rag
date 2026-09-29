from src.config.settings import TOP_K_RESULTS, RERANK_TOP_N, RERANKER_ENABLED
from src.retriever.document_retriever import retrieve_candidates
from src.retriever.query_expander import expand_query
from src.reranker.cross_encoder_reranker import CrossEncoderReranker
from src.reranker.relevance_gate import filter_relevant_results


class RerankedRetriever:

    def __init__(
        self,
        reranker: CrossEncoderReranker | None = None,
    ):
        self.reranker = (
            reranker
            if reranker is not None
            else CrossEncoderReranker()
            if RERANKER_ENABLED
            else None
        )

    def retrieve(
        self,
        query: str,
        k: int = TOP_K_RESULTS,
        top_n: int = RERANK_TOP_N,
    ):
        expanded_query = expand_query(query)

        candidates = retrieve_candidates(
            query=expanded_query,
            k=k,
        )

        if self.reranker is not None:
            ranked = self.reranker.rerank(
                query=expanded_query,
                candidates=candidates,
                top_n=top_n,
            )
        else:
            ranked = candidates[:top_n]

        return filter_relevant_results(ranked)