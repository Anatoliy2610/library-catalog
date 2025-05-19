from app.users.models import UserModel


def get_check_user(email, db):
    data = db.query(UserModel).filter(UserModel.email == email).first()
    if data:
        raise ValueError("Пользователь уже существует")
    