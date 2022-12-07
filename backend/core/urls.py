from fastapi import APIRouter

from backend.core.config import settings

api_router = APIRouter(prefix=settings.API_URL)
