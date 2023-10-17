import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from src.models import Base

db_env = os.environ.get("DB_ENV", "local")
if db_env == "local":
    DATABASE_URL = "sqlite+aiosqlite:///./db/local.db"
elif db_env == "production":
    DATABASE_URL = "sqlite+aiosqlite:///./db/production.db"
else:
    DATABASE_URL = "sqlite+aiosqlite:///./db/test.db"
engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
async_session = AsyncSession(engine, expire_on_commit=False)

# Define your models and their tables using `metadata` as you would with synchronous SQLAlchemy

# To create the tables asynchronously, you should use the `async` version of `create_all` from `metadata`
async def create_tables(engine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.metadata.create_all)

# Call the `create_tables` function using an event loop and ensure it is awaited properly
async def create_db_tables():
    await create_tables(engine, Base)

