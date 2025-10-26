from api.v1.repositories import BaseRepository
from database.models.users.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select, or_, literal, func
from utils.cryptography import hash_password
import settings
from ..exceptions import EntityAlreadyExistsError



class UserRepository(BaseRepository[User]):


    def __init__(self, session: AsyncSession):
        super().__init__(User, session)


    async def create_user(
        self,
        email: str,
        username: str,
        password: str
    ):
        password_hash = hash_password(
            password=password,
            secret_key=settings.APP_SECRET_KEY
        )

        if await self.is_user_exists(
            email=email, username=username
        ):
            raise EntityAlreadyExistsError(
                f"User with email: {email} or username: {username} already exists"
            )

        user = User(
            email=email,
            username=username,
            password_hash=password_hash
        )

        await self.add(
            user
        )

        return user

        
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()
    

    async def is_user_exists(
        self, 
        email: Optional[str] = None, 
        username: Optional[str] = None
    ) -> bool:
        if not email and not username:
            raise ValueError("Either email or username must be provided")

        conditions = []
        if email:
            conditions.append(func.lower(User.email) == func.lower(email))
        if username:
            conditions.append(func.lower(User.username) == func.lower(username))

        stmt = (
            select(literal(True))
            .where(or_(*conditions))
            .limit(1)
        )
        return bool((await self.session.execute(stmt)).scalar())
    

    async def update(self, obj: User, data: dict):
        for field, value in data.items():

            if field == "email":
                raise EntityAlreadyExistsError
            
            if field == "username":
                raise EntityAlreadyExistsError

            if field == "password":
                obj.password_hash = hash_password(password=value)
                continue

            setattr(obj, field, value)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj
    

    async def user_list(self, page: int, size: int):

        query = select(User)

        if page and size:
            query = query.limit(size).offset(page)

        users = await self.session.execute(query)
        users = users.scalars().all()
        return users


