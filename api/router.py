from fastapi import APIRouter
from .v1.router import router as v1


api_router = APIRouter()
api_router.include_router(v1, prefix="/v1")