from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Allows to define database models as Python classes.
Base = declarative_base()


# Obtain, close session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
