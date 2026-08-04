import sqlite3
from pathlib import Path

from repositories.task_repository import Task


class SQLiteTaskRepository:
    def __init__(self):
        self.database_path = (
            Path(__file__).resolve().parent.parent / "tasks.db"
        )

        self.initialize_database()

    def get_connection(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize_database(self):
        with self.get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT 0
                )
                """
            )

            task_count = connection.execute(
                "SELECT COUNT(*) FROM tasks"
            ).fetchone()[0]

            if task_count == 0:
                connection.executemany(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (?, ?)
                    """,
                    [
                        ("Learn FastAPI", 0),
                        ("Build CRUD API", 0),
                        ("Push project to GitHub", 1),
                    ],
                )

            connection.commit()

    @staticmethod
    def convert_row(row: sqlite3.Row) -> Task:
        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
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
                WHERE id = ?
                """,
                (task_id,),
            ).fetchone()

        if row is None:
            return None

        return self.convert_row(row)

    def create(self, title: str) -> Task:
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (?, ?)
                """,
                (title, 0),
            )

            connection.commit()

            task_id = cursor.lastrowid

            row = connection.execute(
                """
                SELECT id, title, done
                FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            ).fetchone()

        return self.convert_row(row)

    def update(
        self,
        task_id: int,
        title: str,
        done: bool,
    ) -> Task | None:
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET title = ?, done = ?
                WHERE id = ?
                """,
                (
                    title,
                    int(done),
                    task_id,
                ),
            )

            if cursor.rowcount == 0:
                return None

            connection.commit()

            row = connection.execute(
                """
                SELECT id, title, done
                FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            ).fetchone()

        return self.convert_row(row)

    def delete(self, task_id: int) -> bool:
        with self.get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            )

            connection.commit()

        return cursor.rowcount > 0