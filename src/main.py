from src.readers.pdf_reader import read_pdf
from src.chunking.text_splitter import split_text
from src.embeddings.embedding_model import embedding_model

print("=" * 60)
print("Loading PDF")
print("=" * 60)

text = read_pdf("data/NDSAP Implementation Guidelines 2.4.pdf")

chunks = split_text(text)

vectors = embedding_model.embed_documents(chunks)

print(f"\nCharacters : {len(text)}")
print(f"Chunks     : {len(chunks)}")
print(f"Vectors    : {len(vectors)}")
print(f"Dimensions : {len(vectors[0])}")

print("\nFirst Chunk:\n")
print(chunks[0][:200])

print("\nFirst Vector (first 10 values):\n")
print(vectors[0][:10])