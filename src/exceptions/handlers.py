from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.custom_exceptions import (
    DocumentNotFound,
    InvalidPDF,
    LLMError,
    TaskNotFound,
    VectorDatabaseError,
)


async def document_not_found_handler(
    request: Request,
    exc: DocumentNotFound,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": {
                "code": "DOCUMENT_NOT_FOUND",
                "message": str(exc),
            },
        },
    )


async def invalid_pdf_handler(
    request: Request,
    exc: InvalidPDF,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "INVALID_PDF",
                "message": str(exc),
            },
        },
    )


async def vector_database_error_handler(
    request: Request,
    exc: VectorDatabaseError,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "VECTOR_DATABASE_ERROR",
                "message": str(exc),
            },
        },
    )


async def llm_error_handler(
    request: Request,
    exc: LLMError,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "LLM_ERROR",
                "message": str(exc),
            },
        },
    )


async def task_not_found_handler(
    request: Request,
    exc: TaskNotFound,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": {
                "code": "TASK_NOT_FOUND",
                "message": str(exc),
            },
        },
    )