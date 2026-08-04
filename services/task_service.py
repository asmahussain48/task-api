from repositories.task_repository import (
    Task,
    TaskRepository,
)


class TaskNotFoundError(Exception):
    pass


class TaskValidationError(Exception):
    pass


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_tasks(self) -> list[Task]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError("Task not found")

        return task

    def create_task(self, body: dict) -> Task:
        title = body.get("title")

        if not isinstance(title, str) or not title.strip():
            raise TaskValidationError(
                "Title is required and cannot be empty"
            )

        return self.repository.create(title.strip())

    def update_task(
        self,
        task_id: int,
        body: dict,
    ) -> Task:
        existing_task = self.repository.get_by_id(task_id)

        if existing_task is None:
            raise TaskNotFoundError("Task not found")

        if not body or not any(
            key in body for key in ["title", "done"]
        ):
            raise TaskValidationError(
                "Provide title or done"
            )

        updated_title = existing_task["title"]
        updated_done = existing_task["done"]

        if "title" in body:
            title = body["title"]

            if not isinstance(title, str) or not title.strip():
                raise TaskValidationError(
                    "Title cannot be empty"
                )

            updated_title = title.strip()

        if "done" in body:
            done = body["done"]

            if not isinstance(done, bool):
                raise TaskValidationError(
                    "Done must be true or false"
                )

            updated_done = done

        updated_task = self.repository.update(
            task_id=task_id,
            title=updated_title,
            done=updated_done,
        )

        if updated_task is None:
            raise TaskNotFoundError("Task not found")

        return updated_task

    def delete_task(self, task_id: int) -> None:
        deleted = self.repository.delete(task_id)

        if not deleted:
            raise TaskNotFoundError("Task not found")