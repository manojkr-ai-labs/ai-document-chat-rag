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

from fastapi.responses import StreamingResponse
from src.services.rag_stream_service import stream_answer
from sqlalchemy.orm import Session
from fastapi import Depends

from src.database.database import get_db
from src.services.conversation_service import ConversationService
from src.services.chat_service import ChatService

from src.background.tasks import (
    create_task,
    process_document,
)
from src.api.schemas import (
    ConversationCreateRequest,
    ConversationRenameRequest,
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


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    start = perf_counter()

    service = ChatService(db)

    result = service.chat(
        question=request.question,
        conversation_id=request.conversation_id,
    )

    execution_time = round(
        perf_counter() - start,
        2,
    )

    return {
        "success": True,
        "message": "Answer generated successfully",
        "data": result,
        "execution_time": execution_time,
    }

@router.post("/chat/stream",
    summary="Stream an answer",
    description="Generate an answer using the indexed documents and stream it token by token.",
    tags=["Chat"],
)
def chat_stream(request: ChatRequest):

    def generate():
        for chunk in stream_answer(request.question):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    ) 

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


# permisted chat
@router.get(
    "/conversations",
    summary="List Conversations",
    tags=["Conversations"],
)
def list_conversations(
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
    return {
            "success": True,
            "message": "All conversations retrieved successfully",
            "data": service.list_conversations()
        } 

@router.get(
    "/conversations/{conversation_id}",
    summary="Get Conversation",
    tags=["Conversations"],
)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)
 
    conversation = service.get_conversation_with_messages(
    conversation_id
)

    if conversation is None:
     raise HTTPException(
        status_code=404,
        detail="Conversation not found",
    )

    return {
        "success": True,
        "message": "Conversation retrieved successfully",
        "data": conversation,
    }

@router.post(
    "/conversations",
    summary="Create Conversation",
    tags=["Conversations"],
)
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    conversation = service.create_conversation(
        request.title,
    )

    return {
        "success": True,
        "message": "Conversation created successfully",
        "data": conversation,
    }

def rename_conversation(
    self,
    conversation_id: str,
    title: str,
):
    conversation = self.get_conversation(conversation_id)

    if conversation is None:
        return None

    return self.conversation_repo.rename(
        conversation,
        title,
    )

@router.patch("/conversations/{conversation_id}")
def rename_conversation(
    conversation_id: str,
    request: ConversationRenameRequest,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    conversation = service.rename_conversation(
        conversation_id,
        request.title,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "success": True,
        "data": conversation,
    }

@router.delete(
    "/conversations/{conversation_id}",
    summary="Delete Conversation",
    tags=["Conversations"],
)
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    deleted = service.delete_conversation(
        conversation_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "success": True,
        "message": "Conversation deleted successfully",
    }