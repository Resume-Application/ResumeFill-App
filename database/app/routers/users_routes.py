from sqlmodel import Session
from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from app.core.db import get_session
from app.models.user_models import UserPublic, User
from app.dependencies.auth_dependencies import get_current_user
from app.services.application_services import count_user_applications
router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]
    
@router.get("/user/profile", response_model=UserPublic)
def get_current_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return current_user


@router.get("/user/summary")
def get_user_summary(
        session: SessionDep,
        current_user: User = Depends(get_current_user)
    ):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    applications_count = count_user_applications(session, current_user.id)

    return {
        "username": current_user.username,
        "profile_url": "to_be_implemented",
        "applications_count": applications_count
    }