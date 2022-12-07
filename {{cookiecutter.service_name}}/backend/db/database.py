import enum
import json
from contextlib import asynccontextmanager
from datetime import datetime
from functools import partial

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings


class DatetimeAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, enum.Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)


custom_serializer = partial(json.dumps, cls=DatetimeAwareJSONEncoder, ensure_ascii=False)


engine = create_async_engine(
    settings.POSTGRESQL_URI,
    connect_args={},
    json_serializer=custom_serializer,
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


@asynccontextmanager
async def in_transaction() -> AsyncSession:
    session = async_session()
    await session.begin()
    try:
        yield session
        await session.commit()
    except BaseException:
        await session.rollback()
        raise
    finally:
        await session.close()
