from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    existing_user = await db.execute(
        select(models.User).filter(
            or_(
                models.User.email == user.email,
                models.User.username == user.username
            )
        )
    )
    existing_user = existing_user.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already exists for another user.")
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, full_name=user.full_name,
                          password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    user = await db.execute(select(models.User).where(models.User.id == user_id))
    return user.scalar()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = select(models.User).offset(skip).limit(limit)
    users = await db.execute(statement)
    return users.scalars()


async def update_user(db: AsyncSession, user_id: int, user: schemas.UserUpdate):
    db_user = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = db_user.scalar_one()
    if db_user:
        if 'email' in vars(user) or 'username' in vars(user):
            existing_user = await db.execute(
                select(models.User).filter(
                    or_(
                        models.User.email == user.email,
                        models.User.username == user.username
                    )
                )
            )
            existing_user = existing_user.scalar_one_or_none()
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email or username already exists for another user.")

            for var, value in vars(user).items():
                if value is not None:
                    setattr(db_user, var, value)
            await db.commit()
            await db.refresh(db_user)
            return db_user


async def delete_user(db: AsyncSession, user_id: int):
    user = await db.execute(select(models.User).where(models.User.id == user_id))
    user = user.scalar()
    if user:
        await db.delete(user)
        await db.commit()
        return user


async def get_user_by_username(db: AsyncSession, username: str):
    user = await db.execute(select(models.User).where(models.User.username == username))
    return user.scalar_one_or_none()
