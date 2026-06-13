from typing import Type
from pydantic import BaseModel


def validator(data:list[dict], model_class:Type[BaseModel]) -> list[dict]:
    if not data:
        return []
    print(data)
    return [model_class.model_validate(record).model_dump() for record in data]
