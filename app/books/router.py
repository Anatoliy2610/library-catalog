from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.books.models import BookModel
from app.books.schemas import BookAdd, BookUpdate, BookDelete, Book
from app.users.auth import get_db
from app.users.user import get_current_user
from app.users.models import UserModel

from app.books.utils import get_check_book, get_check_book_in_db
from app.books.db import add_to_db, update_to_db, delete_to_db


router = APIRouter(tags=['Книги'])


@router.get("/books", response_model=List[Book])
def get_books(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(BookModel).all()


@router.post("/book/add")
def add_to_book(data_book: BookAdd, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        get_check_book(data_book.name, db=db)
        add_to_db(data_book.name, data_book.author, data_book.publication, data_book.ISBN, data_book.count, db=db)
    except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
    return {'Добавлено': {
        'name': data_book.name,
        'author': data_book.author,
        'publication': data_book.publication,
        'ISBN': data_book.ISBN,
        'count': data_book.count
    }}


@router.patch("/book/update")
def update_book(data_book: BookUpdate, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        get_check_book_in_db(book_name=data_book.name, db=db)
        update_to_db(
             book_name=data_book.name,
             publication=data_book.publication, 
             ISBN=data_book.ISBN, 
             count=data_book.count, 
             db=db
             )
   
    except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
    return {'Изменена книга': data_book.name}


@router.delete("/book/delete")
def delete_to_book(data_book: BookDelete, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        get_check_book_in_db(book_name=data_book.name, db=db)
        delete_to_db(book_name=data_book.name, db=db)

    except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )

    return {'Удалено': {
                'name': data_book.name
        }}
