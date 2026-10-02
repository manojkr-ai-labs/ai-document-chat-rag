from src.retriever.document_retriever import retrieve_candidates
from src.reranker.cross_encoder_reranker import CrossEncoderReranker


 
QUERIES = [
    "What is the maximum marks for the BCS-011 examination?",
    "What is IATA Annual?",
    "What is the population of Japan?",
    "What is IIITE?",
]
def main():
    reranker = CrossEncoderReranker()

    for query in QUERIES:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        candidates = retrieve_candidates(
            query,
            k=5,
        )

        print("\n=== BEFORE RERANKING ===")

        for index, candidate in enumerate(candidates, start=1):
            document = candidate.document

            print(
                f"{index}. "
                f"retrieval_score={candidate.retrieval_score:.4f} | "
                f"source={document.metadata.get('source')} | "
                f"page={document.metadata.get('page')}"
            )

        ranked = reranker.rerank(
            query,
            candidates,
        )

        print("\n=== AFTER RERANKING ===")

        for index, candidate in enumerate(ranked, start=1):
            document = candidate.document

            print(
                f"{index}. "
                f"rerank_score={candidate.rerank_score:.4f} | "
                f"source={document.metadata.get('source')} | "
                f"page={document.metadata.get('page')}"
            )

if __name__ == "__main__":
    main()