from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class RetrievalResult:
    document: Document
    retrieval_score: float
    rerank_score: float | None = None