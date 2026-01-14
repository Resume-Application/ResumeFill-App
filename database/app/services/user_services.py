from datetime import timedelta
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select
from app.core import security
from app.core.config import settings
from app.core.db import get_session
from app.models.user_models import User, UserCreate, UserPermission, UserPublic
from app.core.security import hash_password, TokenResponse, create_access_token, verify_password
import logging

logger = logging.getLogger(__name__)
SessionDep = Annotated[Session, Depends(get_session)]

def find_user_with_id(session : SessionDep, user_id : int) -> User | None:
    return session.exec(select(User).where(User.id == user_id)).first()

def find_user_with_name(session : SessionDep, username : str) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()

def find_user_with_email(session : SessionDep, email : str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

def create_user(session : SessionDep, user_in : UserCreate, userPerm : List[str] = None) -> User | None:
    '''
    Creates a user with given permissions and passwords
    
    :param session: FastAPI session
    :type session: SessionDep
    :param user_in: User creation model
    :type user_in: UserCreate
    :param userPerm: List of user permissions to assing the user. Defaults to basic.
    :type userPerm: List[str]
    :return: User or None on valueError.
    :rtype: User | None
    '''
    if userPerm is None:
        userPerm = ["basic"]
    
    if (find_user_with_email(session, user_in.email)):
        logger.error(f"Attempted to create user with existing email: {user_in.email}")
        raise ValueError("The user with this email already exists in the system")
    if (find_user_with_name(session, user_in.username)):
        logger.error(f"Attempted to create user with existing username: {user_in.username}")
        raise ValueError("The user with this username already exists in the system")

    try:
        user = User(
            username= user_in.username,
            hashed_password=hash_password(user_in.password),
            email=user_in.email,
            full_name=user_in.full_name
        )
        session.add(user)
        session.flush()   
        user_id = user.id

        for perm in userPerm:
            user_permission = UserPermission(
                user_id=user_id,
                permission_level=perm
            )
            session.add(user_permission)

        session.commit()
    except Exception as e:
        logger.error(f"Unexpected error {e}")
        raise ValueError(f"Unexpected error {e} while creating user")
    
    return user

def get_user_permissions(session : SessionDep, user_id : int) -> List[UserPermission] | None:
    '''
    Returns a list of user permissions for a given user id.
    
    :param session: FastAPI session
    :type session: SessionDep
    :param user_id: User id
    :type user_id: int
    :return: List of user permissions
    :rtype: List[UserPermission]
    '''
    if find_user_with_id(session, user_id) is None:
        logger.error(f"User id {user_id} not found when getting permissions.")
        raise ValueError("User not found.")
    
    permissions = session.exec(
        select(UserPermission).where(UserPermission.user_id == user_id)
    ).all()

    if len(permissions) == 0:
        logger.warning(f"User id {user_id} has no permissions assigned.")
        raise ValueError("User has no permissions assigned.")
    return permissions