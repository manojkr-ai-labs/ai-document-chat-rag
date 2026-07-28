from time import perf_counter
from unittest import result

from fastapi import APIRouter

from src.api.schemas import BaseResponse, ChatRequest, ChatResponse, HealthData, HealthResponse, HealthResponse, TaskResponse, UploadResponse
from src.services.rag_service import answer_question
from fastapi import UploadFile, File
from src.services.upload_service import save_document, upload_document
from src.services.indexing_api_service import index_documents
from fastapi import BackgroundTasks  
from src.background.tasks import get_task
from fastapi import HTTPException
from src.exceptions.custom_exceptions import DocumentNotFound, TaskNotFound

from src.background.tasks import (
    create_task,
    process_document,
)

router = APIRouter()

@router.get("/health", response_model=HealthResponse,
              summary="Health Check",
              description="Check the health status of the API.",
              tags=["Health"],
              responses={
                200: {"description": "Answer generated successfully"},
                400: {"description": "Invalid request"},
                404: {"description": "Document not found"},
                500: {"description": "Internal server error"},
               },

    )
async def health():
    from src.health.service import check_health
    return {
            "success": True, 
            "data": check_health()
        }


@router.post("/chat",
              response_model=ChatResponse,
             summary="Ask a question",
             description="Generate an answer using the indexed documents.",
             tags=["Chat"],
             responses={
                             200: {"description": "Answer generated successfully"},
                             400: {"description": "Invalid request"},
                             404: {"description": "Document not found"},
                             500: {"description": "Internal server error"},
              },
            
              )
def chat(request: ChatRequest):

    start = perf_counter()

    result = answer_question(request.question)

    execution_time = round(perf_counter() - start, 2)

    return {
        "success": True,
        "message": "Answer generated successfully",
        "data": result,
        "execution_time": execution_time
    }

 

@router.post("/upload", response_model=UploadResponse,
      summary="Upload a document",
      description="Upload and process a document for indexing.",
      tags=["Upload"],
      responses={
                      200: {"description": "Answer generated successfully"},
                      400: {"description": "Invalid request"},
                      404: {"description": "Document not found"},
                      500: {"description": "Internal server error"},
                     }
             )
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), ):
    print("========== UPLOAD HIT ==========")
    content = await file.read()

    result = upload_document(
        file.filename,
        content,
    )

    task_id = create_task()

    background_tasks.add_task(
        process_document,
        task_id,
        result["path"],
    )

    return {
        "success": True,
        "message": "Upload started successfully",
        "data": {
            "task_id": task_id,
            "status": "processing",
            "filename": result["filename"],
        },
    }

@router.post("/index", response_model=BaseResponse,
     summary="Index documents",
     description="Index the uploaded documents for searching.",
     tags=["Indexing"],
    responses={
                     200: {"description": "Answer generated successfully"},
                     400: {"description": "Invalid request"},
                     404: {"description": "Document not found"},
                     500: {"description": "Internal server error"},
                    },
             )
def index(): 
    index_documents()

    return {
        "success": True,
        "message": "Documents indexed successfully"
    }

@router.get("/tasks/{task_id}",  response_model=TaskResponse,
    summary="Get Task Status",
    description="Retrieve the status of a specific task.",
    tags=["Tasks"],
    responses={
                    200: {"description": "Answer generated successfully"},
                    400: {"description": "Invalid request"},
                    404: {"description": "Document not found"},
                    500: {"description": "Internal server error"},
                   },
            )
def task_status(task_id: str):

    task = get_task(task_id)
    
    if task is None:
      raise TaskNotFound("Task not found")

    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": task["status"],
        },
    }