from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.db import get_session
from app.models import User, UserCreate, UserPublic
from app.core.security import hash_password, TokenResponse, create_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/auth/register", response_model=UserPublic)
def register_user(user_in: UserCreate, session : SessionDep):
    # duplication prevention
    user = session.exec(select(User).where(User.username == user_in.username)).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = session.exec(select(User).where(User.email == user_in.email)).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    # try creation
    try:
        user = User(
            username= user_in.username,
            hashed_password=hash_password(user_in.password),
            email=user_in.email,
            full_name=user_in.full_name
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=500,
            detail="Validation error",
        )
    except Exception as e:
        logger.exception(f"Unexpected error {e} while creating user")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        ) 
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/auth/login")
async def auth_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session : SessionDep
) -> TokenResponse:
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if user:
        hashed_password = hash_password(form_data.password)
        if not hashed_password == user.hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return create_access_token(form_data.username, 
                                   timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")