import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
HOST = os.getenv("CLICKHOUSE_HOST")
PORT = os.getenv("CLICKHOUSE_PORT")
DB_NAME = os.getenv("CLICKHOUSE_DB_NAME")
USER = os.getenv("CLICKHOUSE_DB_USER")
PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
SQLALCHEMY_DATABASE_URL = (f"clickhouse+http://{USER}:{PASSWORD}@{HOST}:"
                           f"{PORT}/{DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_olap():
    try:
        yield engine
    finally:
        engine.dispose()
