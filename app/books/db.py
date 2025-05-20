from app.books.models import BookModel


def add_to_db(name, author, publication, ISBN, count, db):
    data = BookModel(
        name=name, author=author, publication=publication, ISBN=ISBN, count=count
    )
    db.add(data)
    db.commit()
    db.refresh(data)


def update_to_db(book_name, publication, ISBN, count, db):
    data = db.query(BookModel).filter(BookModel.name == book_name).first()
    data.publication = publication if publication is not None else data.publication
    data.ISBN = ISBN if ISBN is not None else data.ISBN
    data.count = count if count is not None and count >= 0 else data.count
    db.commit()
    db.refresh(data)


def delete_to_db(book_name, db):
    data = db.query(BookModel).filter(BookModel.name == book_name).first()
    db.delete(data)
    db.commit()
