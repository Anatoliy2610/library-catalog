import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

### SQLite
SQL_BD_URL = os.getenv("SQL_BD_URL")

### POSTGRESQL
# SQL_BD_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQL_BD_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
