from app.books.models import BookModel


def get_check_book(book_name, db):
    data = db.query(BookModel).filter(BookModel.name == book_name).first()
    if data:
        raise ValueError('Книга существует')


def get_check_book_in_db(book_name, db):
    data = db.query(BookModel).filter(BookModel.name == book_name).first()
    if not data:
        raise ValueError('Книга не найдена')
