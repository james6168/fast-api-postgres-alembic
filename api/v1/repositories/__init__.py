from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):


    def __init__(
        self,
        model: Type[ModelType],
        session: AsyncSession
    ):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        return await self.session.get(self.model, id)
    
    
    async def get_all(self) -> List[ModelType]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
    
    async def add(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        return obj
    
    async def update(self, obj: ModelType, data: dict) -> ModelType:
        for field, value in data.items():
            setattr(obj, field, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.commit()




        