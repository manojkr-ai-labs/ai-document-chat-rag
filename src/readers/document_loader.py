from langchain_community.document_loaders import PyPDFLoader


def load_documents(pdf_path):
    """
    Load a single PDF.
    """

    loader = PyPDFLoader(str(pdf_path))

    return loader.load()