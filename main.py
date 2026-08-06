from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

from auth.auth_routes import router as auth_router
from config.supabase_client import get_supabase_client
from routes.task_routes import router as task_router
from routes.auth_routes import router as public_auth_router

app = FastAPI(
    title="Task Afrom fastapi.openapi.utils import get_openapiPI",
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
app.include_router(public_auth_router)

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if isinstance(operation, dict):
                operation["security"] = [
                    {
                        "BearerAuth": []
                    }
                ]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi