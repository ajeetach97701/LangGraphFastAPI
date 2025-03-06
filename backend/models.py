
from sqlmodel import Field, Session, SQLModel, create_engine, select

from pydantic import BaseModel
from typing import List

class User(SQLModel):
    username:str
    email:str | None = None
    full_name :str | None = None
    disabled: bool | None = None
    
        

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str | None = None

class UserInDB(User, table = True):
    id:int | None = Field(default= None, primary_key= True)
    hashed_password: str
    
    
    
    