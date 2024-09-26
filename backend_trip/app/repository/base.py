from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession = None):
        self.session = session or async_session_maker()

    async def find_by_id(self, model_id: int) -> Optional[T]:
        async with self.session as session:
            query = select(self.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def find_one_or_none(self, **filter_by) -> Optional[T]:
        async with self.session as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def find_all(self, **filter_by) -> List[T]:
        async with self.session as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    async def insert_data(self, **data) -> T:
        async with self.session as session:
            query = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()

    async def delete_by_id(self, model_id: int) -> Optional[T]:
        async with self.session as session:
            query = delete(self.model).where(self.model.id == model_id).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()
