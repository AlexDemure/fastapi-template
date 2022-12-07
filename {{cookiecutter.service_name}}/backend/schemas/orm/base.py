from typing import TypeVar

from pydantic import BaseModel

CreateBaseSchemaType = TypeVar("CreateBaseSchemaType", bound=BaseModel)


class UpdatedBaseSchema(BaseModel):
    id: int
    updated_fields: dict
