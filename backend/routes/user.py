from fastapi import APIRouter, Depends
from auth.auth_handler import get_current_active_user
from schemas import *
from models import *
from typing import Annotated

router = APIRouter()
@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user