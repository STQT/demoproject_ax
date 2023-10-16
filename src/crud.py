from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = await db.execute(select(models.User).where(models.User.username == user.username))
    db_user = db_user.first()
    if db_user:
        pass
    else:
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(username=user.username, email=user.email, full_name=user.full_name, password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user


async def get_user(db: AsyncSession, user_id: int):
    return await db.execute(models.User.select().where(models.User.id == user_id))


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = select(models.User).offset(skip).limit(limit)
    users = await db.execute(statement)
    return users

async def update_user(db: AsyncSession, user_id: int, user: schemas.UserUpdate):
    db_user = await db.execute(models.User.select().where(models.User.id == user_id))
    db_user = db_user.first()
    if db_user:
        for var, value in vars(user).items():
            if value is not None:
                setattr(db_user, var, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    user = await db.execute(models.User.select().where(models.User.id == user_id))
    user = user.first()
    if user:
        db.delete(user)
        await db.commit()
        return user


async def search_user_by_name(db: AsyncSession, name: str):
    return await db.execute(models.User.select().where(models.User.username == name))
