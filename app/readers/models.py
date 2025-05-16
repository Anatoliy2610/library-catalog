from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String

from app.database import Base


class Reader(BaseModel):
    name: str
    email: EmailStr


class ReaderModel(Base):
    __tablename__ = 'readers'

    name = Column(String)
    email = Column(String, primary_key=True)

