from time import perf_counter
from unittest import result

from fastapi import APIRouter

from src.api.schemas import ChatRequest
from src.services.rag_service import answer_question
from fastapi import UploadFile, File
from src.services.upload_service import save_document, upload_document
from src.services.indexing_api_service import index_documents
from fastapi import BackgroundTasks  
from src.background.tasks import get_task
from fastapi import HTTPException
from src.exceptions.custom_exceptions import DocumentNotFound

from src.background.tasks import (
    create_task,
    process_document,
)

router = APIRouter()

@router.get("/health")
async def health():
    from src.health.service import check_health
    return {
            "success": True, 
            "data": check_health()
        }

    return 

@router.post("/chat")
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


# @router.post("/upload")
# async def upload(file: UploadFile = File(...)):

@router.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), ):

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

@router.post("/index")
def index(): 
    index_documents()

    return {
        "success": True,
        "message": "Documents indexed successfully"
    }

@router.get("/tasks/{task_id}")
def task_status(task_id: str):

    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": task["status"],
        },
    }