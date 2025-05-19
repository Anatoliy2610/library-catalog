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
    name: str = None
    new_email: EmailStr = None


class ReaderDelete(ReaderBase):
    pass
