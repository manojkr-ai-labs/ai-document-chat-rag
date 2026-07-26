from pydantic import BaseModel


# ---------- Requests ----------

class ChatRequest(BaseModel):
    question: str


# ---------- Common ----------

class Citation(BaseModel):
    source: str
    page: str | int


class BaseResponse(BaseModel):
    success: bool
    message: str | None = None


# ---------- Chat ----------

class ChatData(BaseModel):
    answer: str
    citations: list[Citation]


class ChatResponse(BaseResponse):
    data: ChatData


# ---------- Upload ----------

class UploadData(BaseModel):
    task_id: str
    status: str
    filename: str


class UploadResponse(BaseResponse):
    data: UploadData

class TaskData(BaseModel):
    task_id: str
    status: str


class TaskResponse(BaseResponse):
    data: TaskData

class HealthCheck(BaseModel):
    healthy: bool
    model: str | None = None
    documents: int | None = None
    free_gb: int | float | None = None


class HealthData(BaseModel):
    healthy: bool
    checks: dict[str, HealthCheck]


class HealthResponse(BaseResponse):
    data: HealthData        