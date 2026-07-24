from pathlib import Path
from src.services.indexing_service import index_single_document

DOCUMENTS_DIR = Path("documents")


def save_document(file_name: str, content: bytes) -> str:
    """
    Save uploaded PDF into documents directory.
    """

    DOCUMENTS_DIR.mkdir(exist_ok=True)

    file_path = DOCUMENTS_DIR / file_name

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)
def upload_document(file_name: str, content: bytes):
    """
    Save uploaded PDF and immediately index it.
    """

    file_path = save_document(
        file_name=file_name,
        content=content,
    )

    indexed = index_single_document(file_path)

    return {
        "filename": file_name,
        "path": file_path,
        "indexed": indexed,
    }