from fastapi import FastAPI

from app.books.router import router as router_books
from app.borrowed_books.router import router as router_borrow
from app.database import Base, engine
from app.readers.router import router as router_readers
from app.users.router import router as router_users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_users)
app.include_router(router_books)
app.include_router(router_readers)
app.include_router(router_borrow)
