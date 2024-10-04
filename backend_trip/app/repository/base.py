from sqlalchemy import delete, insert, select, update

from app.core.database import async_session_maker


class BaseRepository:
    model = None

    @classmethod
    async def find_by_id(self, model_id: int):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def insert_data(self, **data):
        async with async_session_maker() as session:
            query = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()

    @classmethod
    async def update_data(cls, model_id: int, **data):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == model_id)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(self, model_id: int):
        async with async_session_maker() as session:
            query = delete(self.model).where(self.model.id == model_id).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()
