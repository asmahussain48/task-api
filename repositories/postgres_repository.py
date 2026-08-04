import os
from typing import Any, Mapping

import psycopg
from psycopg.rows import dict_row

from repositories.task_repository import Task


class PostgresTaskRepository:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise RuntimeError(
                "DATABASE_URL is missing from the environment"
            )

    def get_connection(self):
        return psycopg.connect(
            self.database_url,
            row_factory=dict_row,
        )

    @staticmethod
    def convert_row(row: Mapping[str, Any]) -> Task:
        return {
            "id": row["id"],
            "title": row["title"],
            "done": row["done"],
        }

    def get_all(self) -> list[Task]:
        with self.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, title, done
                FROM tasks
                ORDER BY id
                """
            ).fetchall()

        return [self.convert_row(row) for row in rows]

    def get_by_id(self, task_id: int) -> Task | None:
        with self.get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, title, done
                FROM tasks
                WHERE id = %s
                """,
                (task_id,),
            ).fetchone()

        if row is None:
            return None

        return self.convert_row(row)

    def create(self, title: str) -> Task:
        with self.get_connection() as connection:
            row = connection.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, FALSE)
                RETURNING id, title, done
                """,
                (title,),
            ).fetchone()

        if row is None:
            raise RuntimeError("Task could not be created")

        return self.convert_row(row)

    def update(
        self,
        task_id: int,
        title: str,
        done: bool,
    ) -> Task | None:
        with self.get_connection() as connection:
            row = connection.execute(
                """
                UPDATE tasks
                SET title = %s,
                    done = %s
                WHERE id = %s
                RETURNING id, title, done
                """,
                (
                    title,
                    done,
                    task_id,
                ),
            ).fetchone()

        if row is None:
            return None

        return self.convert_row(row)

    def delete(self, task_id: int) -> bool:
        with self.get_connection() as connection:
            row = connection.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                RETURNING id
                """,
                (task_id,),
            ).fetchone()

        return row is not None
