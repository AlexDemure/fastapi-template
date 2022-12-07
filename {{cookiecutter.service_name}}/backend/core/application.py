import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from backend.core.config import settings
from backend.core.urls import api_router

logger = get_logger()

app = FastAPI(version="2.0", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == "__main__":
    # Лог со всеми настройками системы
    attrs = vars(settings)
    attrs_to_str = "\n".join("%s: %s" % item for item in attrs.items())
    logger.info(f"SETUP ENVS:\n{attrs_to_str}")

    uvicorn.run("application:app", host="127.0.0.1", port=7040, log_level="debug")
