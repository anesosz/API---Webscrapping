"""API Router for Fast API."""
from fastapi import APIRouter

from src.api.routes import hello, data, parameters

router = APIRouter()

router.include_router(hello.router, tags=["Hello"])
router.include_router(data.router, tags=["Dataset handling"])
router.include_router(parameters.router, tags=["Firestore Parameters"])
