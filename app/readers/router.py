from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.readers.models import Reader, ReaderModel
from app.readers.schemas import ReaderAdd, ReaderUpdate, ReaderDelete
from app.users.utils import get_db, get_current_user
from app.users.models import UserModel


router = APIRouter(tags=['Читатели'])


@router.get("/readers", response_model=List[Reader])
# def get_books(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def get_readers(db: Session = Depends(get_db)):
    return db.query(ReaderModel).all()


@router.post("/reader/add")
# def add_to_reader(data_book: ReaderAdd, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def add_to_reader(data_reader: ReaderAdd, db: Session = Depends(get_db)):
    check_reader = db.query(ReaderModel).filter(ReaderModel.email == data_reader.email).first()
    if check_reader:
        return HTTPException(status_code=401, detail={'Инф': 'Читатель существует'})
    db_reader = ReaderModel(
        name = data_reader.name,
        email = data_reader.email,
        )
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return {'Добавлено': {
            'name': db_reader.name,
            'email': db_reader.email,
    }}


@router.patch("/reader/update")
# def update_reader(data_book: ReaderUpdate, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def update_reader(data_reader: ReaderUpdate, db: Session = Depends(get_db)):
    check_reader = db.query(ReaderModel).filter(ReaderModel.email == data_reader.email).first()
    if not check_reader:
        return HTTPException(status_code=401, detail={'Инф': 'Читатель не найден'})
    check_reader.name = data_reader.name if data_reader.name is not None else check_reader.name
    check_reader.email = data_reader.new_email if data_reader.new_email is not None else check_reader.email
    db.commit()
    db.refresh(check_reader)
    return {'Изменен читатель': check_reader}


@router.delete("/reader/delete")
# def delete_to_reader(data_book: ReaderDelete, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
def delete_to_reader(data_reader: ReaderDelete, db: Session = Depends(get_db)):
    db_book = db.query(ReaderModel).filter(ReaderModel.email == data_reader.email).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return {'Читатель удалён': {
                'name': db_book.name,
                'email': db_book.email
        }}
    return HTTPException(status_code=401, detail={'Инф': 'Читатель не найден'}) 
