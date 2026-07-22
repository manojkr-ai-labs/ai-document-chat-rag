 


from src.utils.file_utils import get_pdf_files

pdf_files = get_pdf_files()

print("\nPDF Files Found:\n")

for pdf in pdf_files:
    print(pdf.name)