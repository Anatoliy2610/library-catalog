from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.users.auth import create_access_token, get_db
from app.users.db import add_to_db
from app.users.models import User, UserAuthModel, UserModel
from app.users.schemas import UserRegister
from app.users.security import password_hash, verify_password
from app.users.utils import get_check_user

router = APIRouter(tags=["Пользователь"])


@router.get("/users", response_model=List[User])
def register(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.post("/register")
def register_user(user_data: UserRegister, db: Session = Depends(get_db)) -> dict:
    try:
        get_check_user(email=user_data.email, db=db)
        add_to_db(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash(user_data.password),
            db=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login")
def auth_user(user_data: UserAuthModel, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное email или пароль"
        )
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "refresh_token": None}
