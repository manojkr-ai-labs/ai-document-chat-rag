from src.readers.document_loader import load_documents

documents = load_documents()

# print("=" * 60)
# print("DOCUMENT LOADER TEST")
# print("=" * 60)

# print(f"Total Documents : {len(documents)}")
# print()

# print("Metadata:")
# print(documents[0].metadata)

# print()

# print("Preview:")
# print(documents[0].page_content[:300])
print("Source :", documents[0].metadata["source"])
print("Page   :", documents[0].metadata["page"])
print("Pages  :", documents[0].metadata["total_pages"])