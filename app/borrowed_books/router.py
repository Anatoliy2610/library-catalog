from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Annotated
from datetime import datetime

from app.borrowed_books.models import BorrowedBooksModel
from app.borrowed_books.schemas import BorrowedBooks, BorrowedBooksAdd, BorrowedBooksRemove, BorrowedBooksReader
from app.users.utils import get_db, get_current_user
from app.users.models import UserModel
from app.books.models import BookModel
from app.readers.models import ReaderModel




router = APIRouter(tags=['Выдача и возврат книг'])


@router.get("/borrows", response_model=List[BorrowedBooks])
# def get_books(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def get_borrows(db: Session = Depends(get_db)):
    return db.query(BorrowedBooksModel).all()


@router.post("/borrows/add")
# def add_to_borrows(data_borrow: BorrowedBooksAdd, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def add_to_borrows(data_borrow: BorrowedBooksAdd, db: Session = Depends(get_db)):
    check_book = db.query(BookModel).filter(BookModel.id == data_borrow.book_id).first()
    if not check_book:
        return HTTPException(status_code=401, detail={'Инф': 'Такой книги не существует'})

    check_reader = db.query(ReaderModel).filter(ReaderModel.id == data_borrow.reader_id).first()
    if not check_reader:
        return HTTPException(status_code=401, detail={'Инф': 'Такого читателя не существует'})

    check_count_book = db.query(BorrowedBooksModel).filter(
        BorrowedBooksModel.reader_id == data_borrow.reader_id,
        BorrowedBooksModel.return_date == None).all()
    if len(check_count_book) >= 3:
        return HTTPException(status_code=401, detail={'Инф': 'Читатель не может взять больше книг'})

    if check_book.count == 0:
        return HTTPException(status_code=401, detail={'Инф': 'Такой книги нет в наличии'})
    
    db_borrow = BorrowedBooksModel(
        book_id = data_borrow.book_id,
        reader_id = data_borrow.reader_id
    )

    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    db_book = db.query(BookModel).filter(BookModel.id == data_borrow.book_id).first()
    db_book.count -= 1
    db.commit()
    db.refresh(db_book)
    return {'Выдана книга': {
        'name_book': db_borrow.book_id,
        'name_reader': db_borrow.reader_id,
        'borrow_date': db_borrow.borrow_date
        }}


@router.post("/borrows/remove")
# def add_to_book(data_book: BookAdd, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def remove_to_borrows(data_borrow: BorrowedBooksRemove, db: Session = Depends(get_db)):
    check_book = db.query(BookModel).filter(BookModel.id == data_borrow.book_id).first()
    if not check_book:
        return HTTPException(status_code=401, detail={'Инф': 'Такой книги не существует'})

    check_reader = db.query(ReaderModel).filter(ReaderModel.id == data_borrow.reader_id).first()
    if not check_reader:
        return HTTPException(status_code=401, detail={'Инф': 'Такого читателя не существует'})

    db_borrow = db.query(BorrowedBooksModel).filter(
            BorrowedBooksModel.book_id == data_borrow.book_id,
            BorrowedBooksModel.reader_id == data_borrow.reader_id,
            BorrowedBooksModel.return_date == None).first()
    if not db_borrow:
        return HTTPException(status_code=401, detail={'Инф': 'Эта книга возвращена'})
    
    db_borrow.return_date = datetime.now()
    db.commit()
    db.refresh(db_borrow)
    db_book = db.query(BookModel).filter(BookModel.id == data_borrow.book_id).first()
    db_book.count += 1
    db.commit()
    db.refresh(db_book)
    return {'Возвращена книга': {
        'name_book': db_borrow.book_id,
        'name_reader': db_borrow.reader_id,
        'return_date': db_borrow.return_date
        }}


@router.get("/borrows/reader/{reader_id}", response_model=List[BorrowedBooks])
# def get_books(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def get_borrows(reader_id: Annotated[int, Path(title='Здесь указывается id поста', ge=1, lt=100)], db: Session = Depends(get_db)):
    return db.query(BorrowedBooksModel).filter(BorrowedBooksModel.reader_id == reader_id).all()
