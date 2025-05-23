from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class BorrowedBooksModel(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    borrow_date = Column(String, default=datetime.now)
    return_date = Column(String, nullable=True, default=None)

    book = relationship("BookModel")
    reader = relationship("ReaderModel")
