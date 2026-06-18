from typing import Type
from pydantic import BaseModel


def validator(data:list[dict], model_class:Type[BaseModel]) -> list[dict]:
    if not data:
        return []
    return [model_class.model_validate(record, from_attributes=True).model_dump() for record in data]
