from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(
    title="AI Document Chat API",
    description="Enterprise AI Document Chat Backend",
    version="2.0.0",
)

app.include_router(router)