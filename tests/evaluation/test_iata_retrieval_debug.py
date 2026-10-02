from src.retriever.reranked_retriever import RerankedRetriever


QUERIES = [
    "What is IATA Annual?",
    "IATA Annual",
    "What is IATA Annual General Meeting?",
    "What does the IATA Annual General Meeting address?",
    "IATA General Meeting",
]


def test_iata_retrieval_debug():
    retriever = RerankedRetriever()

    for query in QUERIES:
        print("\n" + "=" * 100)
        print(f"QUERY: {query}")
        print("=" * 100)

        results = retriever.retrieve(
            query=query,
        )

        if not results:
            print("NO RESULTS")
            continue

        for rank, result in enumerate(
            results,
            start=1,
        ):
            document = result.document

            print(f"\nRANK: {rank}")

            print(
                f"RERANK SCORE: "
                f"{result.rerank_score}"
            )

            print(
                f"SOURCE: "
                f"{document.metadata.get('source')}"
            )

            print(
                f"PAGE: "
                f"{document.metadata.get('page')}"
            )

            print("\nCONTENT:")
            print(
                document.page_content
            )