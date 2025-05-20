from app.readers.models import ReaderModel


def get_check_reader(email, db):
    data = db.query(ReaderModel).filter(ReaderModel.email == email).first()
    if data:
        raise ValueError("Читатель существует")


def get_check_reader_in_db(email, db):
    data = db.query(ReaderModel).filter(ReaderModel.email == email).first()
    if not data:
        raise ValueError("Читатель не найден")


def get_check_new_email(new_email, db):
    data = db.query(ReaderModel).filter(ReaderModel.email == new_email).first()
    if data:
        raise ValueError("Читатель с таким email уже существует")
