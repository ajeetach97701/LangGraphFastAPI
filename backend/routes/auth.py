from fastapi import APIRouter, Depends
from contextlib import asynccontextmanager
from db import create_db_and_tables
from models import *
from typing import Annotated
from db import *
from auth.auth_handler import *


@asynccontextmanager
async def lifespan(app: APIRouter):
    create_db_and_tables()
    yield
    
router = APIRouter(lifespan=lifespan)
router = APIRouter()

    
@router.post("/register", response_model= UserResponse)
async def register_user(user:UserCreate, db:Annotated[Session, Depends(get_session)]):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already Exist. Please enter another username")
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(username=user.username, email=user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token")
async def login_for_access_token(
    db: Annotated[Session, Depends(get_session)],
    form_data :Annotated[OAuth2PasswordRequestForm, Depends()],
):
    print("Authenticate user")
    user = authenticate_user(db, username=form_data.username, password=form_data.password)
    print(form_data.username)
    if not user:
        print("here")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expre = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub": user.username}, expires_delta=access_token_expre)
    return Token(access_token=access_token, token_type="bearer")    
    