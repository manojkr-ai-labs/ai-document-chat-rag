from sentence_transformers import CrossEncoder

from src.retriever.retrieval_result import RetrievalResult


MODEL_NAME = "BAAI/bge-reranker-base"


class CrossEncoderReranker:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        top_n: int | None = None,
    ) -> list[RetrievalResult]:

        if not candidates:
            return []

        pairs = [
            (
                query,
                candidate.document.page_content,
            )
            for candidate in candidates
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(candidates, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        if top_n is not None:
            ranked = ranked[:top_n]

        return [
            RetrievalResult(
                document=candidate.document,
                retrieval_score=candidate.retrieval_score,
                rerank_score=float(score),
            )
            for candidate, score in ranked
        ]