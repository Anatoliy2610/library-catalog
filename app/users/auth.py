from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from jose import JWTError
from dotenv import load_dotenv
import os

from app.database import SessionLocal
from app.users.pass_conf import verify_password
from app.users.models import UserModel


load_dotenv()
SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or verify_password(plain_password=password, hashed_password=user.hash_password) is False:
        return None
    return user


def get_auth_data():
    return {"secret_key": SECRET_KEY_TOKEN, "algorithm": 'HS256'}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm='HS256')
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY_TOKEN, algorithms=['HS256'])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
           )
