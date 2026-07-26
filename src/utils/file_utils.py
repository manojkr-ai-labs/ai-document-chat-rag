from pathlib import Path
from src.config.settings import DOCUMENTS_DIR 

def get_pdf_files(data_folder: str = DOCUMENTS_DIR) -> list[Path]:
    """
    Return all PDF files from the data folder.
    """

    folder = Path(data_folder)

    if not folder.exists():
        raise FileNotFoundError(f"{data_folder} folder not found.")

    
    pdf_files = sorted(folder.rglob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
                f"No PDF files found in '{folder.resolve()}'."
            ) 
    

    return pdf_files