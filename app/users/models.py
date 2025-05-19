from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String
from app.database import Base


class User(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String)
    hash_password = Column(String, nullable=True)


class UserAuthModel(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Пароль")
