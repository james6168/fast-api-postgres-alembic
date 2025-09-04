from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/test")
async def test():
    return {"testing_endpoint": "ok"}