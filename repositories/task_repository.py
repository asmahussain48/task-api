from typing import Protocol, TypedDict


class Task(TypedDict):
    id: int
    title: str
    done: bool


class TaskRepository(Protocol):
    def get_all(self) -> list[Task]:
        ...

    def get_by_id(self, task_id: int) -> Task | None:
        ...

    def create(self, title: str) -> Task:
        ...

    def update(
        self,
        task_id: int,
        title: str,
        done: bool,
    ) -> Task | None:
        ...

    def delete(self, task_id: int) -> bool:
        ...