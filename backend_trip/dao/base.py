from sqlalchemy import delete, insert, select

from database import async_session_maker


class BaseDAO:
    model = None

    # READ
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    # CREATE
    @classmethod
    async def insetr_data(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    # DELETE
    @classmethod
    async def delete_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == model_id).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()
