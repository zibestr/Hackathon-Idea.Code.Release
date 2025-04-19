from sqlmodel import SQLModel
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlacodegen.generators import DeclarativeGenerator
from contextlib import asynccontextmanager
import aiofiles

from typing import AsyncGenerator, Callable
from utils import logs
from config import settings

DB_URI = f'postgresql+asyncpg://{settings.postgres_db_user}:{settings.postgres_db_password}' \
         f'@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db_name}'
connect_args = {"check_same_thread": False}
engine = create_async_engine(DB_URI)
make_session: Callable = sessionmaker(bind=engine, class_=AsyncSession)


@logs
async def create_models(models_filename: str):
    metadata = MetaData()
    async with engine.connect() as conn:
        await conn.run_sync(metadata.reflect)

    generator = DeclarativeGenerator(
        metadata,
        bind=engine,
        options=["use_inflect"]     # склонение имён
    )

    async with aiofiles.open(models_filename, 'w', encoding='utf-8') as models_file:
        await models_file.write(generator.generate())


@logs
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@logs
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with make_session() as session:
        yield session
