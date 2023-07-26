"""
Basic database engine setup
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.helpers import create_db_url


SQLALCHEMY_DATABASE_URL = create_db_url()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False,
                            bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
