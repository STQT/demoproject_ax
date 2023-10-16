from typing import List

from src import crud, models, schemas
from src.database import async_session, engine

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Function to get the database session
async def get_db():
    async with async_session as session:
        yield session


# Creating a user
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_user


# Getting a user by id
@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Getting all users
@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip, limit)
    print(users, "########")
    return list(users)


# Updating a user by id
@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# Deleting a user by id
@app.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Searching for a user by name
@app.get("/users/search/{name}", response_model=List[schemas.User])
async def search_user_by_name(name: str, db: AsyncSession = Depends(get_db)):
    users = await crud.search_user_by_name(db, name)
    return users
