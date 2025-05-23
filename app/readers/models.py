from sqlalchemy import Column, Integer, String

from app.database import Base


class ReaderModel(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
