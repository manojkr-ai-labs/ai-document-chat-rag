from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Citation(BaseModel):
    source: str
    page: str | int


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]