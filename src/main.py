from src.readers.document_loader import load_documents
from src.chunking.text_splitter import split_documents

documents = load_documents()

chunks = split_documents(documents)

print("=" * 60)
print("DOCUMENT CHUNKING TEST")
print("=" * 60)

print(f"Original Pages : {len(documents)}")
print(f"Chunks         : {len(chunks)}")

print()
print("Metadata:")
print(chunks[0].metadata)

print()
print("Preview:")
print(chunks[0].page_content[:300])