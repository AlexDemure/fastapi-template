from typing import AsyncGenerator

from backend.db.database import in_transaction


async def db_session() -> AsyncGenerator:
    async with in_transaction() as db:
        yield db
