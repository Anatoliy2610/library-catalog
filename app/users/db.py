from app.users.models import UserModel


def add_to_db(username, email, password_hash, db):
    data = UserModel(username=username, email=email, hash_password=password_hash)
    db.add(data)
    db.commit()
    db.refresh(data)
