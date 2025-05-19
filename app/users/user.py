from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.users.auth import get_db
from app.users.token import (check_authorization, parse_authorization_header, 
                       decode_jwt_token, validate_token_type, 
                       validate_token_expiration, get_user_from_db)


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    check_authorization(authorization)
    token_type, access_token = parse_authorization_header(authorization)
    payload = decode_jwt_token(access_token)
    validate_token_type(token_type)
    validate_token_expiration(payload)
    user = get_user_from_db(payload, db)
    return user
