from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.readers.models import ReaderModel
from app.readers.schemas import Reader, ReaderAdd, ReaderUpdate, ReaderDelete
from app.users.auth import get_db
from app.users.user import get_current_user
from app.users.models import UserModel
from app.readers.utils import get_check_reader, get_check_reader_in_db, get_check_new_email
from app.readers.db import add_to_db, update_to_db, delete_to_db


router = APIRouter(tags=['Читатели'])


@router.get("/readers", response_model=List[Reader])
def get_readers(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(ReaderModel).all()


@router.post("/reader/add")
def add_to_reader(data_reader: ReaderAdd, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        get_check_reader(email=data_reader.email, db=db)
        add_to_db(name=data_reader.name, email=data_reader.email, db=db)
    except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
    return {'Добавлено': {
            'name': data_reader.name,
            'email': data_reader.email
    }}


@router.patch("/reader/update")
def update_reader(data_reader: ReaderUpdate, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        get_check_reader_in_db(email=data_reader.email, db=db)
        get_check_new_email(new_email=data_reader.new_email, db=db)
        update_to_db(
            name=data_reader.name,
            email=data_reader.email,
            new_email=data_reader.new_email,
            db=db)
    except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )

    return {'Изменен читатель': data_reader.name}


@router.delete("/reader/delete")
def delete_to_reader(data_reader: ReaderDelete, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        get_check_reader_in_db(email=data_reader.email, db=db)
        delete_to_db(email=data_reader.email, db=db)
    except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
    
    return {'Читатель удалён': {
                'name': data_reader.name,
                'email': data_reader.email
        }}
 