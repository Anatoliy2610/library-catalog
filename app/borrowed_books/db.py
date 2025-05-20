from datetime import datetime

from app.books.models import BookModel
from app.borrowed_books.models import BorrowedBooksModel


def add_to_db(book_id, reader_id, db):
    data = BorrowedBooksModel(book_id=book_id, reader_id=reader_id)
    db.add(data)
    db.commit()
    db.refresh(data)


def change_db_book(book_id, db, value):
    data = db.query(BookModel).filter(BookModel.id == book_id).first()
    data.count += value
    db.commit()
    db.refresh(data)


def get_return_date(book_id, reader_id, db):
    data = (
        db.query(BorrowedBooksModel)
        .filter(
            BorrowedBooksModel.book_id == book_id,
            BorrowedBooksModel.reader_id == reader_id,
            BorrowedBooksModel.return_date == None,
        )
        .first()
    )
    data.return_date = datetime.now()
    db.commit()
    db.refresh(data)
