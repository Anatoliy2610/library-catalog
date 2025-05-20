from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.borrowed_books.db import add_to_db, change_db_book, get_return_date
from app.borrowed_books.models import BorrowedBooksModel
from app.borrowed_books.schemas import (BorrowedBooks, BorrowedBooksAdd,
                                        BorrowedBooksRemove)
from app.borrowed_books.utils import (get_check_book, get_check_count_book,
                                      get_check_count_book_for_reader,
                                      get_check_issuance, get_check_reader)
from app.users.auth import get_db
from app.users.models import UserModel
from app.users.user import get_current_user

router = APIRouter(tags=["Выдача и возврат книг"])


@router.get("/borrows", response_model=List[BorrowedBooks])
def get_borrows(
    user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    return db.query(BorrowedBooksModel).all()


@router.post("/borrows/add")
def add_to_borrows(
    data_borrow: BorrowedBooksAdd,
    user_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        get_check_book(book_id=data_borrow.book_id, db=db)
        get_check_count_book(book_id=data_borrow.book_id, db=db)
        get_check_reader(reader_id=data_borrow.reader_id, db=db)
        get_check_count_book_for_reader(reader_id=data_borrow.reader_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    add_to_db(book_id=data_borrow.book_id, reader_id=data_borrow.reader_id, db=db)
    change_db_book(data_borrow.book_id, db=db, value=(-1))
    return {
        "Выдана книга": {
            "name_book": data_borrow.book_id,
            "name_reader": data_borrow.reader_id,
        }
    }


@router.post("/borrows/remove")
def remove_to_borrows(
    data_borrow: BorrowedBooksRemove,
    user_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        get_check_book(book_id=data_borrow.book_id, db=db)
        get_check_reader(reader_id=data_borrow.reader_id, db=db)
        get_check_issuance(data_borrow.book_id, data_borrow.reader_id, db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    get_return_date(data_borrow.book_id, data_borrow.reader_id, db=db)
    change_db_book(data_borrow.book_id, db=db, value=1)
    return {
        "Возвращена книга": {
            "name_book": data_borrow.book_id,
            "name_reader": data_borrow.reader_id,
        }
    }


@router.get("/borrows/reader/{reader_id}", response_model=List[BorrowedBooks])
def get_books(
    reader_id: Annotated[int, Path(title="Здесь указывается id поста", ge=1, lt=100)],
    user_data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(BorrowedBooksModel)
        .filter(BorrowedBooksModel.reader_id == reader_id)
        .all()
    )
