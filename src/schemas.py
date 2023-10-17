import re

from pydantic import BaseModel, EmailStr, validator, Field


class UserBase(BaseModel):
    username: str = Field("username", min_length=3, max_length=50)
    email: EmailStr = Field("example@gmail.com")
    full_name: str = Field("Gayrat Sultonov")

    @validator("username")
    def check_username_format(cls, v):
        regEx = r"^[a-zA-Z0-9_-]+$"
        if not re.search(regEx, v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
        return v


class User(UserBase):
    id: int


class UserCreate(UserBase):
    password: str = Field("hashed_password", min_length=6, max_length=100)


class UserAuth(BaseModel):
    username: str = Field("Username", min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    full_name: str = None


class AccessToken(BaseModel):
    access_token: str
    token_type: str