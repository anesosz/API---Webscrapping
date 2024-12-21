from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.api.router import router_v1


app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom handler for 404 errors.

    Args:
        request (Request): The incoming HTTP request.
        exc (StarletteHTTPException): The exception instance.

    Returns:
        JSONResponse: A meaningful error message.
    """
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Resource not found",
                "detail": f"The URL {request.url.path} does not exist."
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

def get_application() -> FastAPI:
    application = FastAPI(
        title="epf-flower-data-science",
        description="""Fast API""",
        version="1.0.0",
        redoc_url=None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router_v1)
    return application


app = get_application()

def custom_openapi():
    """
    Customize the OpenAPI schema for Swagger.

    Adds a `Bearer Token` authentication scheme.

    Returns:
        dict: The customized OpenAPI schema.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="EPF Flower Data Science",
        version="1.0.0",
        description="API for managing authentication and user roles.",
        routes=app.routes,
    )


    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }


    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi
