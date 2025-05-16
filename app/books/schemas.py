from pydantic import BaseModel, Field
from typing import Optional


class BookAdd(BaseModel):
    name: str
    author: str
    publication: int = None
    ISBN: str = None
    count: int = Field(..., description="Количество экземпляров", ge=0)


class BookUpdate(BaseModel):
    name: str
    publication: int = None
    ISBN: str = None
    count: int = None


class BookDelete(BaseModel):
    name: str



