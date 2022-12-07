import os
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgresql+asyncpg"}


class PostgresDBSettings(BaseSettings):

    POSTGRESQL_URI: Optional[AsyncPostgresDsn] = None

    @validator("POSTGRESQL_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v
        # Return URL-connect 'postgresql://postgres:catcatdog@postgres/catcatdog'
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "password"),
            host=os.environ.get("POSTGRES_SERVER", "localhost"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
            path=f"/{os.environ.get('POSTGRES_DB', 'db')}",
        )
