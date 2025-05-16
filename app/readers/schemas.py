from pydantic import BaseModel, EmailStr


class ReaderAdd(BaseModel):
    name: str
    email: EmailStr


class ReaderUpdate(BaseModel):
    name: str = None
    email: EmailStr
    new_email: EmailStr = None


class ReaderDelete(BaseModel):
    email: EmailStr
