from fastapi import APIRouter, Depends
from app.models.user_models import UserPublic, User
from app.dependencies.auth_dependencies import get_current_user

router = APIRouter()

@router.get("/user/profile", response_model=UserPublic)
def get_current_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return current_user
