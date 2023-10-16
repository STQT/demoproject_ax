from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    full_name: str = None

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
