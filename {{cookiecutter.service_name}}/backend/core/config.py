import os

from backend.db.settings import PostgresDBSettings

# INCLUDE SETTINGS
configs = [PostgresDBSettings]


class Settings(*configs):  # type:ignore
    ENV: str = os.environ.get("ENV", "DEV")
    SERVER: str = os.environ.get("SERVER", "http")
    DOMAIN: str = os.environ.get("DOMAIN", "127.0.0.1")
    API_URL: str = "/api"

    class Config:
        case_sensitive = True


settings = Settings()
