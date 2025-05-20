from datetime import datetime, timezone

import jwt
from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.users.auth import get_auth_data
from app.users.models import UserModel


def check_authorization(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")


def parse_authorization_header(authorization: str):
    try:
        token_type, access_token = authorization.split()
        return token_type, access_token
    except ValueError:
        raise HTTPException(status_code=401, detail="Неправильный заголовок")


def decode_jwt_token(access_token: str):
    auth_data = get_auth_data()
    try:
        payload = jwt.decode(
            access_token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный!"
        )
    return payload


def validate_token_type(token_type: str):
    if token_type != "Bearer":
        raise HTTPException(status_code=401, detail="Неправильный тип токена")


def validate_token_expiration(payload: dict):
    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
        )


def get_user_from_db(payload: dict, db: Session):
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя"
        )
    user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
