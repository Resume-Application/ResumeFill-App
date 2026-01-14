from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import decode_access_token
from app.models.user_models import User
from app.services.user_services import find_user_with_id
import logging

logger = logging.getLogger(__name__)
SessionDep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_access_token(token)
    except Exception as e:
        logger.error(f"Exception {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int | None = payload.user_id
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user claim",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = find_user_with_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user