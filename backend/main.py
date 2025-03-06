from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, List


from contextlib import asynccontextmanager
from db import create_db_and_tables
from models import *
from db import *
from auth.auth_handler import *


    




origins = [
    "*"
    "127.0.0.1:3000",
    "https://localhost:8000",
]

from routes.auth import router as auth_router
from routes.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan = lifespan)
app.include_router(user_router)
app.include_router(auth_router, prefix="/auth")


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# memory_db = {"fruits":[]}

# @app.get("/fruits", response_model=Fruits)
# def get_fruits():
#     return Fruits(fruits=memory_db['fruits'])


# @app.post("/fruits", response_model=Fruit)
# def add_fruit(fruit:Fruit):
#     memory_db["fruits"].append(fruit)
#     return fruit