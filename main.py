import asyncio
from datetime import timedelta
from typing import List

from src import crud, schemas, authentication
from src.authentication import verify_password
from src.database import async_session, create_db_tables

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(debug=True)


async def get_db():
    async with async_session as session:
        yield session


@app.post("/auth", response_model=schemas.AccessToken)
async def login(user_request: schemas.UserAuth, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_username(db, user_request.username)
    is_correct_password = verify_password(user_request.password, user.password)
    if not user or not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db, user)
    return db_user


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/", response_model=List[schemas.UserBase])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip, limit)
    return users


@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/users/{user_id}", response_model=None)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return None


@app.get("/users/search/{username}", response_model=schemas.User)
async def search_user_by_name(username: str, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.on_event("startup")
async def startup_event():
    await create_db_tables()


@app.on_event("shutdown")
async def shutdown_event():
    await async_session.close()
