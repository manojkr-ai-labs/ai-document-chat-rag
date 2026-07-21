from src.readers.pdf_reader import read_pdf
from src.chunking.text_splitter import split_text

text = read_pdf("data/NDSAP Implementation Guidelines 2.4.pdf")

chunks = split_text(text)

print("=" * 60)
print("DOCUMENT INFORMATION")
print("=" * 60)

print(f"Total Characters : {len(text)}")
print(f"Total Chunks     : {len(chunks)}")

print("\n" + "=" * 60)
print("CHUNK 1")
print("=" * 60)
print(chunks[0])

print("\n" + "=" * 60)
print("CHUNK 2")
print("=" * 60)
print(chunks[1])