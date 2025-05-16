from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr


class UserDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Пароль")
