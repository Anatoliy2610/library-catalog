from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    name: str
    author: str
    publication: Optional[int] = None
    ISBN: Optional[str] = None
    count: int = Field(..., description="Количество экземпляров", ge=0)



class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookAdd(BookBase):
    pass


class BookUpdate(BookBase):
    author: str = None
    publication: int = None
    ISBN: str = None
    count: int = None


class BookDelete(BaseModel):
    name: str
