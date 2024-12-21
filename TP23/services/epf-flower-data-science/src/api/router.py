"""API Router for Fast API."""
from fastapi import APIRouter

from src.api.routes import hello, data, parameters, authentication

# Step 19: API versioning
router_v1 = APIRouter(prefix="/v1")

router_v1 .include_router(hello.router, tags=["Hello"])
router_v1 .include_router(data.router, tags=["Dataset handling"])
router_v1 .include_router(parameters.router, tags=["Firestore Parameters"])
router_v1 .include_router(authentication.router, tags=["Authentication"])
