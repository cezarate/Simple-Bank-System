""" This is the database file.

It initializes the engine for the database.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from bank.settings import settings


SQLALCHEMY_DATABASE_URL = f"sqlite:///./{settings.db_name}.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def SessionManager():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        