from fastapi import APIRouter
from .endpoints.users import users


router = APIRouter()
router.include_router(users.router)