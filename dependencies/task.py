from repositories.postgres_repository import PostgresTaskRepository
from services.task_service import TaskService


task_repository = PostgresTaskRepository()

task_service = TaskService(
    task_repository
)


def get_task_service():
    return task_service