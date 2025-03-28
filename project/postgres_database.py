import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project.postgres.base import Base

load_dotenv()
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB_NAME")
USER = os.getenv("POSTGRES_DB_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:"
                           f"{PORT}/{DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    print(f"Initializing database URL: {SQLALCHEMY_DATABASE_URL}")
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
