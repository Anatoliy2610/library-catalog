from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from app.database import Base


class Book(BaseModel):
    name: str
    author: str
    publication: int | None
    ISBN: str | None
    count: int


class BookModel(Base):
    __tablename__ = 'books'

    name = Column(String, primary_key=True)
    author = Column(String)
    publication = Column(Integer)
    ISBN = Column(String)
    count = Column(Integer)
