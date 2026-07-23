from src.retriever.retriever import retrieve_context

from src.utils.logger import logger
query = input("Ask: ")

results = retrieve_context(query)

print()

for i, (doc, score) in enumerate(results, start=1):
    logger.info(f"{i}. {doc.metadata['source']} | "f"Page {doc.metadata.get('page')} | " f"Score {score:.4f}")
    print("=" * 60)
    print(f"Result {i}")
    print(f"Score : {score:.4f}")
    print(f"Source: {doc.metadata['source']}")
    print()
    print(doc.page_content[:250])
    print()
  