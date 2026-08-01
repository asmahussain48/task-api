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
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Push project to GitHub", "done": True},
]


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
    return tasks


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(body: dict):
    title = body.get("title")

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": False,
    }

    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, body: dict):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None,
    )

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    if not body or not any(key in body for key in ["title", "done"]):
        return JSONResponse(
            status_code=400,
            content={"error": "Provide title or done"},
        )

    if "title" in body:
        title = body["title"]

        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"},
            )

        task["title"] = title.strip()

    if "done" in body:
        if not isinstance(body["done"], bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"},
            )

        task["done"] = body["done"]

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
)
def delete_task(task_id: int):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None,
    )

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    tasks.remove(task)
    return Response(status_code=204)