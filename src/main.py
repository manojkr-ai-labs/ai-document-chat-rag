from src.readers.pdf_reader import read_pdf

text = read_pdf("data/NDSAP Implementation Guidelines 2.4.pdf")

print("=" * 60)
print("PDF PREVIEW")
print("=" * 60)

print(text[:1000])