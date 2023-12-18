from collections.abc import Sequence
from typing import TypeVar

import sqlalchemy as sa

from app.src.services.db.base import session_factory


T = TypeVar("T")


class BaseDAO:
    @classmethod
    async def find_all(cls, model: type[T], **filter_by) -> Sequence[T]:
        async with session_factory() as session:
            query = sa.select(model).filter_by(**filter_by)
            response = await session.scalars(query)
            return response.all()

    @classmethod
    async def find_one_or_none(cls, model: type[T], **filter_by) -> T | None:
        async with session_factory() as session:
            query = sa.select(model).filter_by(**filter_by)
            response = await session.scalar(query)
            return response

    @classmethod
    async def add(cls, model: type[T], **data) -> T:
        async with session_factory() as session:
            # session.add(model)
            query = sa.insert(model).values(**data).returning(model)
            response = await session.execute(query)
            await session.commit()
            return response.scalar_one()

    @classmethod
    async def delete(cls, model, **filter_by):
        async with session_factory() as session:
            query = sa.delete(model).where(**filter_by)
            await session.execute(query)
            await session.commit()

