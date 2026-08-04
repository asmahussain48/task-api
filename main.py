from fastapi import FastAPI

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
        "endpoints": ["/tasks"],
    }


@app.get("/health", summary="Check API health")
def health_check():
    return {"status": "ok"}


app.include_router(task_router)