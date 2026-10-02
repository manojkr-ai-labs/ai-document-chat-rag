from src.retriever.reranked_retriever import RerankedRetriever


query = "What is the maximum marks for the BCS-011 examination?"

retriever = RerankedRetriever()

results = retriever.retrieve(query=query)

print("\n" + "=" * 80)
print(f"QUERY: {query}")
print("=" * 80)

for rank, result in enumerate(results, start=1):
    print(f"\nRANK: {rank}")
    print(f"RERANK SCORE: {result.rerank_score}")

    print(
        "SOURCE:",
        result.document.metadata.get("source"),
    )

    print(
        "PAGE:",
        result.document.metadata.get("page"),
    )

    print("\nCONTENT:")
    print(result.document.page_content)

    print("-" * 80)