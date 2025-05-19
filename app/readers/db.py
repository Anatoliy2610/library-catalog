from app.readers.models import ReaderModel


def add_to_db(name, email, db):
    data = ReaderModel(
        name = name,
        email = email
        )
    db.add(data)
    db.commit()
    db.refresh(data)


def update_to_db(name, email, new_email, db):
    data = db.query(ReaderModel).filter(ReaderModel.email == email).first()
    data.name = name if name is not None else data.name
    data.email = new_email if new_email is not None else data.email
    db.commit()
    db.refresh(data)


def delete_to_db(email, db):
    data =  db.query(ReaderModel).filter(ReaderModel.email == email).first()
    db.delete(data)
    db.commit()
