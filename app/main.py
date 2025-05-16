from fastapi import FastAPI

from app.users.router import router as router_users
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_users)
