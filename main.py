import sqlite3
from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Task API",
    version="1.0",
)
DATABASE_PATH = Path(__file__).resolve().parent / "tasks.db"


def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_database_connection() as connection:
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
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Learn FastAPI", 0),
                    ("Build CRUD API", 0),
                    ("Push project to GitHub", 1),
                ],
            )

        connection.commit()


initialize_database()
def convert_task_row(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
    }

@app.get("/", summary="Show API information")
def get_api_information():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health", summary="Check API health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    with get_database_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            ORDER BY id
            """
        ).fetchall()

    return [convert_task_row(row) for row in rows]


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    with get_database_connection() as connection:
        row = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    return convert_task_row(row)


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(body: dict):
    title = body.get("title")

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    with get_database_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            (title.strip(), 0),
        )

        connection.commit()

        new_task_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = ?
            """,
            (new_task_id,),
        ).fetchone()

    return convert_task_row(row)


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, body: dict):
    with get_database_connection() as connection:
        existing_task = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()

        if existing_task is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"},
            )

        if not body or not any(
            key in body for key in ["title", "done"]
        ):
            return JSONResponse(
                status_code=400,
                content={"error": "Provide title or done"},
            )

        updated_title = existing_task["title"]
        updated_done = bool(existing_task["done"])

        if "title" in body:
            title = body["title"]

            if not isinstance(title, str) or not title.strip():
                return JSONResponse(
                    status_code=400,
                    content={"error": "Title cannot be empty"},
                )

            updated_title = title.strip()

        if "done" in body:
            if not isinstance(body["done"], bool):
                return JSONResponse(
                    status_code=400,
                    content={"error": "Done must be true or false"},
                )

            updated_done = body["done"]

        connection.execute(
            """
            UPDATE tasks
            SET title = ?, done = ?
            WHERE id = ?
            """,
            (
                updated_title,
                int(updated_done),
                task_id,
            ),
        )

        connection.commit()

        updated_task = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()

    return convert_task_row(updated_task)


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
)
def delete_task(task_id: int):
    with get_database_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        )

        if cursor.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"},
            )

        connection.commit()

    return Response(status_code=204)