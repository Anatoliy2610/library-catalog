from fastapi import FastAPI

from app.database import Base, engine
from app.users.router import router as router_users
from app.books.router import router as router_books
from app.readers.router import router as router_readers
from app.borrowed_books.router import router as router_borrow


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_users)
app.include_router(router_books)
app.include_router(router_readers)
app.include_router(router_borrow)
