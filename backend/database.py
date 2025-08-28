from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .utils.secret_data import DATABASE_URL, TEST_DATABASE_URL, TEST_MODE

class Base(DeclarativeBase):
    pass

engine = create_engine(url=TEST_DATABASE_URL) if TEST_MODE else create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()