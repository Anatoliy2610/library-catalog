from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session

from app.users.utils import (get_db, get_password_hash, verify_password, create_access_token, get_current_user)
from app.users.models import UserModel, UserAuthModel, User
from app.users.schemas import UserRegister


router = APIRouter(tags=['Пользователь'])


@router.get("/users", response_model=List[User])
async def register(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.post("/register/")
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)) -> dict:
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hash_password = get_password_hash(user_data.password)
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: UserAuthModel, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if user is None or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное email или пароль'
        )
    access_token = create_access_token({"sub": str(user.id)})
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(user_data: UserModel = Depends(get_current_user)):
    return user_data
