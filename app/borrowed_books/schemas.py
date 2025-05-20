from pydantic import BaseModel

from app.books.schemas import Book
from app.readers.schemas import Reader


class BorrowedBooksBase(BaseModel):
    book_id: int
    reader_id: int


class BorrowedBooks(BorrowedBooksBase):
    id: int
    book: Book
    reader: Reader
    borrow_date: str
    return_date: str | None

    class Config:
        orm_mode = True


class BorrowedBooksAdd(BorrowedBooksBase):
    pass


class BorrowedBooksRemove(BorrowedBooksBase):
    book_id: int


class BorrowedBooksReader(BaseModel):
    reader_id: int
