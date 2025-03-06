import jwt
from fastapi import Depends, HTTPException, status, APIRouter
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
load_dotenv()
from db import get_session

from models import *

from schemas import *

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
SessinDep = Annotated[Session, Depends(get_session)]

router = APIRouter()




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password:str):
    return pwd_context.hash(plain_password)


def get_user(db:Session, username:str):
    # db_user = db.get(User, username)
    print("Here")
    db_user = db.exec(select(UserInDB).where(UserInDB.username == username)).first()
    print(db_user)
    return db_user

def authenticate_user(db:Session, username:str, password:str):
    user = get_user(db, username)
    print(user);print()
    if not user:
        print(False)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict, expires_delta:timedelta | None = None ):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode, key= SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

async def get_current_user(token:str = Depends(oauth2_scheme), db:Session = (Depends(get_session))):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username = username)
    except InvalidTokenError:
        raise credential_exception
    user = db.exec(select(UserInDB).where(UserInDB.username == token_data.username)).first()
    if user is None:
        raise credential_exception
    return user
    
async def get_current_active_user(current_user:Annotated[User, Depends(get_current_user)]):
    return current_user