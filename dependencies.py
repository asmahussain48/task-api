from repositories.sqlite_repository import (
    SQLiteTaskRepository,
)
from services.task_service import TaskService


task_repository = SQLiteTaskRepository()

task_service = TaskService(task_repository)


def get_task_service() -> TaskService:
    return task_service