from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.api.router import router


app = FastAPI()



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

    application.include_router(router)
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