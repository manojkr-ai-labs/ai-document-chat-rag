 
from src.services.indexing_service import build_vector_database

def index_documents():
    """
    Trigger document indexing.
    """
    build_vector_database()