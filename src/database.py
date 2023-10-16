import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./db/test.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
async_session = AsyncSession(engine, expire_on_commit=False)

Base = declarative_base()

# Define your models and their tables using `metadata` as you would with synchronous SQLAlchemy

# To create the tables asynchronously, you should use the `async` version of `create_all` from `metadata`
async def create_tables(engine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.metadata.create_all)

# Call the `create_tables` function using an event loop and ensure it is awaited properly
async def main():
    await create_tables(engine, Base)

# Run the event loop using `loop.run_until_complete` to execute the main coroutine
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
