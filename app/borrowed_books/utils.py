from app.books.models import BookModel
from app.borrowed_books.models import BorrowedBooksModel
from app.readers.models import ReaderModel


def get_check_book(book_id, db):
    data = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not data:
        raise ValueError("Такой книги не существует")


def get_check_count_book(book_id, db):
    data = db.query(BookModel).filter(BookModel.id == book_id).first()
    if data.count == 0:
        raise ValueError("Такой книги нет в наличии")


def get_check_reader(reader_id, db):
    data = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if not data:
        raise ValueError("Такого читателя не существует")


def get_check_count_book_for_reader(reader_id, db):
    data = (
        db.query(BorrowedBooksModel)
        .filter(
            BorrowedBooksModel.reader_id == reader_id,
            BorrowedBooksModel.return_date == None,
        )
        .all()
    )
    if len(data) >= 3:
        raise ValueError("Читатель не может взять больше книг")


def get_check_issuance(book_id, reader_id, db):
    data = (
        db.query(BorrowedBooksModel)
        .filter(
            BorrowedBooksModel.book_id == book_id,
            BorrowedBooksModel.reader_id == reader_id,
            BorrowedBooksModel.return_date == None,
        )
        .first()
    )
    if not data:
        raise ValueError("У читателя нет такой книги, она уже возвращена")
