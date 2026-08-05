from fastapi import FastAPI

from auth.auth_routes import router as auth_router
from config.supabase_client import get_supabase_client
from routes.task_routes import router as task_router


app = FastAPI(
    title="Task API",
    version="1.0",
)


@app.get("/", summary="Show API information")
def get_api_information():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks",
            "/auth/signup",
            "/auth/login",
        ],
    }


@app.get("/health", summary="Check API health")
def health_check():
    return {
        "status": "ok",
    }


app.include_router(task_router)

app.include_router(auth_router)