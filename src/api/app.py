from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.exceptions.custom_exceptions import (
    DocumentNotFound,
    InvalidPDF,
    LLMError,
    TaskNotFound,
    VectorDatabaseError,
)
from src.exceptions.handlers import (
    document_not_found_handler,
    invalid_pdf_handler,
    llm_error_handler,
    task_not_found_handler,
    vector_database_error_handler,
)
from src.middleware.request_logger import RequestLoggingMiddleware


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app = FastAPI(
    title="AI Document Chat API",
    description="Enterprise AI Document Chat Backend",
    version="2.0.0",
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

app.add_exception_handler(
    TaskNotFound,
    task_not_found_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Conversation-ID"],
)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(router)