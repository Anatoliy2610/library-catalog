from typing import Optional

from pydantic import BaseModel, EmailStr


class ReaderBase(BaseModel):
    name: str
    email: EmailStr


class Reader(ReaderBase):
    id: int

    class Config:
        orm_mode = True


class ReaderAdd(ReaderBase):
    pass


class ReaderUpdate(ReaderBase):
    name: Optional[str] = None
    new_email: Optional[EmailStr] = None


class ReaderDelete(ReaderBase):
    pass
