from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.db import get_session
from app.models.user_models import User, UserCreate, UserPublic
from app.core.security import hash_password, TokenResponse, create_access_token, verify_password
from app.services.user_services import find_user_with_email, find_user_with_name, create_user

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/auth/register", response_model=UserPublic)
def register_user(user_in: UserCreate, session : SessionDep):
    
    try:
        user = create_user(session, user_in)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str("User creation failed"))

    return user

@router.post("/auth/login")
async def auth_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session : SessionDep
) -> TokenResponse:
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if user:
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        user_id = user.id
        return create_access_token(user_id, 
                                   timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")