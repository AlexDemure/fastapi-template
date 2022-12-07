from typing import Generic, List, Optional, Type

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.models.base import ModelType
from backend.schemas.orm.base import CreateBaseSchemaType, UpdatedBaseSchema


async def one_or_none(api_db: AsyncSession, query: Select) -> Optional[ModelType]:
    return (await api_db.execute(query)).scalars().one_or_none()


async def get_list(api_db: AsyncSession, query: Select) -> List[ModelType]:
    return (await api_db.execute(query)).scalars().all()


async def get_total_rows(api_db: AsyncSession, query: Select) -> int:
    return (await api_db.execute(select(func.count()).select_from(query.subquery()))).scalars().one()


class CRUDBase(Generic[ModelType, CreateBaseSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, api_db: AsyncSession, data: CreateBaseSchemaType) -> ModelType:
        new_object = self.model(**data.dict())
        api_db.add(new_object)
        await api_db.flush()
        await api_db.refresh(new_object)
        return new_object

    async def get(self, api_db: AsyncSession, object_id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == object_id)
        return await one_or_none(api_db, query)

    async def update(self, api_db: AsyncSession, data: UpdatedBaseSchema) -> None:
        query = update(self.model).where(self.model.id == data.id).values(**data.updated_fields)
        await api_db.execute(query)
        await api_db.flush()

    async def delete(self, api_db: AsyncSession, object_id: int) -> None:
        query = delete(self.model).where(self.model.id == object_id)
        await api_db.execute(query)
        await api_db.flush()
