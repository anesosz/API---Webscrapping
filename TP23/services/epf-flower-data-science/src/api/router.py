"""API Router for Fast API."""
from fastapi import APIRouter

from src.api.routes import hello, data, parameters, authentication

router = APIRouter()

router.include_router(hello.router, tags=["Hello"])
router.include_router(data.router, tags=["Dataset handling"])
router.include_router(parameters.router, tags=["Firestore Parameters"])
router.include_router(authentication.router, tags=["Authentication"])
