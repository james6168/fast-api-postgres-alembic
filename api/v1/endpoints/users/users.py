from fastapi import APIRouter, Depends, HTTPException, Query, Path
from database import get_session
from database.models.auth.user import User
from api.v1.schemes.users.users import BaseUserScheme, UserOutScheme, UpdateUserScheme
from utils.cryptography import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from api.v1.repositories.users.users import UserRepository
from api.v1.repositories.exceptions import EntityAlreadyExistsError


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create")
async def user_create(
    payload: BaseUserScheme,
    db_session: AsyncSession = Depends(get_session)
):

    repo = UserRepository(session=db_session)

    try:
        user = await repo.create_user(
            email=payload.email,
            password=payload.password,
            username=payload.username
        )

        return {
            "user": UserOutScheme.model_validate(
                user.as_dict()
            ).model_dump(
                exclude_unset=True
            )
        }

    except EntityAlreadyExistsError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )



@router.patch("/update/{user_id}")
async def user_update(
    payload: UpdateUserScheme,
    db_session: AsyncSession = Depends(get_session),
    user_id: int = Path(..., gt=0)
):
    user = await db_session.get(User, user_id)
    repo = UserRepository(db_session)

    if not user:
        raise HTTPException(
            status_code=404, 
            detail={
                "error": f"User with provided id: {user_id} not found"
            }
        )
    
    user = await repo.update(
        obj=user,
        data=payload.model_dump(exclude_unset=True)
    )

    return {
        "user": UserOutScheme.model_validate(user.as_dict()).model_dump(exclude_unset=True)
    }



@router.get("/list")
async def get_users(
    db_session: AsyncSession = Depends(get_session),
    page: Optional[int] = Query(None, gt=0),
    size: Optional[int] = Query(None, gt=9, lt=100),
    
):
    repo = UserRepository(db_session)
    users = await repo.user_list(page=page, size=size)

    return {
        "page": page,
        "size": size,
        "users": [
            UserOutScheme.model_validate(
                user.as_dict()
            ).model_dump(exclude_unset=True) 
            for user in users
        ]
    }




