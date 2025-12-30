from fastapi import APIRouter, Request
from app.models import UserPublic

router = APIRouter()

@router.get("/user/profile", response_model=UserPublic)
def read_users_me(request: Request):
    return request.state.user
