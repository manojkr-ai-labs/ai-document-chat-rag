from fastapi import APIRouter

router = APIRouter()


@router.get("/health") 
def health():
    return {
        "status": "healthy",
        "service": "AI Document Chat",
        "version": "2.0.0"
    }