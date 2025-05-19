from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, CheckConstraint, orm

from app.database import Base


class BookModel(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    author = Column(String)
    publication = Column(Integer)
    ISBN = Column(String)
    count = Column(Integer, CheckConstraint('count >= 0'))

    @orm.validates('count')
    def validate_count(self, key, value):
        if value < 0:
            raise ValueError(f'Invalid age {value}')
        return value
