from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from dependencies import get_task_service
from services.task_service import (
    TaskNotFoundError,
    TaskService,
    TaskValidationError,
)


router = APIRouter()





@router.get("/tasks", summary="List all tasks")
def get_tasks(
    service: TaskService = Depends(get_task_service),
):
    return service.get_tasks()


@router.get("/tasks/{task_id}", summary="Get one task")
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.get_task(task_id)

    except TaskNotFoundError as error:
        return JSONResponse(
            status_code=404,
            content={"error": str(error)},
        )


@router.post(
    "/tasks",
    status_code=201,
    summary="Create a new task",
)
def create_task(
    body: dict,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.create_task(body)

    except TaskValidationError as error:
        return JSONResponse(
            status_code=400,
            content={"error": str(error)},
        )


@router.put(
    "/tasks/{task_id}",
    summary="Update a task",
)
def update_task(
    task_id: int,
    body: dict,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.update_task(task_id, body)

    except TaskNotFoundError as error:
        return JSONResponse(
            status_code=404,
            content={"error": str(error)},
        )

    except TaskValidationError as error:
        return JSONResponse(
            status_code=400,
            content={"error": str(error)},
        )


@router.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    try:
        service.delete_task(task_id)
        return Response(status_code=204)

    except TaskNotFoundError as error:
        return JSONResponse(
            status_code=404,
            content={"error": str(error)},
        )