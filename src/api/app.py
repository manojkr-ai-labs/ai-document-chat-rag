from fastapi import FastAPI

from src.api.routes import router
from src.middleware.request_logger import RequestLoggingMiddleware

from src.exceptions.custom_exceptions import (
    DocumentNotFound,
    InvalidPDF,
    VectorDatabaseError,
    LLMError,
)

from src.exceptions.handlers import (
    document_not_found_handler,
    invalid_pdf_handler,
    vector_database_error_handler,
    llm_error_handler,
)

app = FastAPI(
    title="AI Document Chat API",
    description="Enterprise AI Document Chat Backend",
    version="2.0.0",
      contact={
        "name": "Manoj Kumar Sah",
        "email": "...",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_exception_handler(
    DocumentNotFound,
    document_not_found_handler,
)

app.add_exception_handler(
    InvalidPDF,
    invalid_pdf_handler,
)

app.add_exception_handler(
    VectorDatabaseError,
    vector_database_error_handler,
)

app.add_exception_handler(
    LLMError,
    llm_error_handler,
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(router)