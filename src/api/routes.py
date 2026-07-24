from time import perf_counter

from fastapi import APIRouter

from src.api.schemas import ChatRequest
from src.services.rag_service import answer_question
from fastapi import UploadFile, File
from src.services.upload_service import save_document

router = APIRouter()


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

@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    content = await file.read()

    path = save_document(
        file.filename,
        content
    )

    return {
        "success": True,
        "message": "File uploaded successfully",
        "data": {
            "filename": file.filename,
            "path": path
        }
    }