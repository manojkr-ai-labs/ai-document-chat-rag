from pathlib import Path

from src.config.settings import DOCUMENTS_DIR


def save_document(file_name: str, content: bytes) -> str:
    """
    Save uploaded PDF into documents directory.
    """
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    safe_file_name = Path(file_name).name

    if not safe_file_name.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed")

    file_path = DOCUMENTS_DIR / safe_file_name

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)


def upload_document(file_name: str, content: bytes):
    """
    Save uploaded PDF only.
    Indexing will happen in the background.
    """
    file_path = save_document(
        file_name=file_name,
        content=content,
    )

    return {
        "filename": file_name,
        "path": file_path,
    }