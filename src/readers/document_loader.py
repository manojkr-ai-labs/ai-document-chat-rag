from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from src.utils.file_utils import get_pdf_files

def load_documents() -> list[Document]:
    """
    Load every PDF from the documents folder.

    Returns:
        list[Document]
    """

    pdf_files = get_pdf_files()

    documents = []

    for pdf in pdf_files:
        loader = PyPDFLoader(str(pdf))
        documents.extend(loader.load())

    return documents