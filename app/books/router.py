from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.books.models import Book, BookModel
from app.books.schemas import BookAdd, BookUpdate, BookDelete
from app.users.utils import get_db, get_current_user
from app.users.models import UserModel


router = APIRouter(tags=['Книги'])


@router.get("/books", response_model=List[Book])
# def get_books(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def get_books(db: Session = Depends(get_db)):
    return db.query(BookModel).all()


@router.post("/book/add")
# def add_to_book(data_book: BookAdd, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def add_to_book(data_book: BookAdd, db: Session = Depends(get_db)):
    check_book = db.query(BookModel).filter(BookModel.name == data_book.name).first()
    if check_book:
        return HTTPException(status_code=401, detail={'Инф': 'Книга существует'})
    db_book = BookModel(
        name = data_book.name,
        author = data_book.author,
        publication = data_book.publication,
        ISBN = data_book.ISBN,
        count = data_book.count

        )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {'Добавлено': {
            'name': data_book.name,
            'author': data_book.author,
            'publication': data_book.publication,
            'ISBN': data_book.ISBN,
            'count': data_book.count,
    }}


@router.patch("/book/update")
# def update_book(data_book: BookDelete, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def update_book(data_book: BookUpdate, db: Session = Depends(get_db)):
    check_book = db.query(BookModel).filter(BookModel.name == data_book.name).first()
    if not check_book:
        return HTTPException(status_code=401, detail={'Инф': 'Книга не найдена'})

    check_book.publication = data_book.publication if data_book.publication is not None else check_book.publication
    check_book.ISBN = data_book.ISBN if data_book.ISBN is not None else check_book.ISBN
    check_book.count = data_book.count if data_book.count is not None else check_book.count
    db.commit()
    db.refresh(check_book)
    return {'Изменена книга': check_book}


@router.delete("/book/delete")
# def delete_to_book(data_book: BookDelete, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def delete_to_book(data_book: BookDelete, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.name == data_book.name).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return {'Удалено': {
                'name': data_book.name
        }}
    return HTTPException(status_code=401, detail={'Инф': 'Книга не найдена'}) 
