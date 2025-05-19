from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.main import app
from app.database import Base
from app.users.auth import get_db
from app.users.models import UserModel
from app.users.user import get_current_user


def cleanup():
    try:
        os.remove("test.db")
    except OSError as e:
        print(f"Ошибка при удалении файла тестовой базы данных: {e}")

cleanup()


client = TestClient(app)

def override_get_current_user():
    test_user = UserModel(id=1, username="test", email='test@example.com', hash_password='test_password')
    return test_user


app.dependency_overrides[get_current_user] = override_get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def get_json_book(name, author, count, publication=None, ISBN=None):
    return {
        "name": name,
        "author": author,
        "publication": publication,
        "ISBN": ISBN,
        "count": count
    }


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200


def test_add_to_book():
    response = client.post("/book/add", json=get_json_book(name="test_book", author="test_author", count=5, publication=2010, ISBN="test_ISBN"))
    assert response.status_code == 200
    response = client.post("/book/add", json=get_json_book(name="test_book2", author="test_author", count=0))
    assert response.status_code == 200
    response = client.post("/book/add", json=get_json_book(name="test_book", author="test_author", count=0))
    assert response.status_code == 401


def get_json_reader(name, email):
    return {
        "name": name,
        "email": email
    }


def test_get_readers():
    response = client.get("/readers")
    assert response.status_code == 200


def test_add_to_reader():
    response = client.post("/reader/add", json=get_json_reader(name='test_name', email='test_email@example.com'))
    assert response.status_code == 200
    response = client.post("/reader/add", json=get_json_reader(name='test_name', email='test_email2@example.com'))
    assert response.status_code == 200
    response = client.post("/reader/add", json=get_json_reader(name='test_name2', email='test_email2@example.com'))
    assert response.status_code == 401


def get_json_borrow(book_id, reader_id):
    return {
        "book_id": book_id,
        "reader_id": reader_id
    }


def test_get_borrows():
    response = client.get("/borrows")
    assert response.status_code == 200


def test_add_to_borrows():
    response = client.post("/borrows/add", json=get_json_borrow(book_id=1, reader_id=1))
    assert response.status_code == 200
    response = client.post("/borrows/add", json=get_json_borrow(book_id=1, reader_id=1))
    assert response.status_code == 200
    response = client.post("/borrows/add", json=get_json_borrow(book_id=1, reader_id=1))
    assert response.status_code == 200
    response = client.post("/borrows/add", json=get_json_borrow(book_id=1, reader_id=1))
    assert response.status_code == 401
    response = client.post("/borrows/add", json=get_json_borrow(book_id=30, reader_id=1))
    assert response.status_code == 401
    response = client.post("/borrows/add", json=get_json_borrow(book_id=1, reader_id=30))
    assert response.status_code == 401
    response = client.post("/borrows/add", json=get_json_borrow(book_id=2, reader_id=1))
    assert response.status_code == 401
