import uuid

from src.services.indexing_service import index_single_document
from src.utils.logger import logger

tasks = {}


def create_task():
    """
    Create a new background task.
    """

    task_id = str(uuid.uuid4())

    tasks[task_id] = {
        "status": "processing",
    }

    return task_id


def complete_task(task_id):
    """
    Mark task as completed.
    """

    if task_id in tasks:
        tasks[task_id]["status"] = "completed"


def failed_task(task_id):
    """
    Mark task as failed.
    """

    if task_id in tasks:
        tasks[task_id]["status"] = "failed"


def get_task(task_id):
    """
    Return task information.
    """

    return tasks.get(task_id)


def process_document(task_id: str, file_path: str):
    """
    Background worker for indexing a PDF.
    """

    try:
        index_single_document(file_path)
        complete_task(task_id)

    except Exception:
        logger.exception(
            "Failed to process document: %s",
            file_path,
        )
        failed_task(task_id)