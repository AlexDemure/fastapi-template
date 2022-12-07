from typing import TypeVar

from backend.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
