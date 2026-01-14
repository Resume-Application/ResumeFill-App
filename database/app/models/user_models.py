from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from pydantic import BaseModel
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    disabled: bool | None = False



class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    email: str | None = Field(default=None, index=True)
    full_name: str | None = None

class UserPermission(SQLModel, table=True):
    '''
    Defines what class of permissions a user has.
    '''
    id: int | None = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="user.id", index=True)
    permission_level: str
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
class UserPublic(UserBase):
    profile_img : str = "Default.png"

class UserLogin(BaseModel):
    '''Credentials for logging in'''
    username :str
    password:str


class UserCreate(BaseModel):
    '''
    JSON model for creating a user
    '''
    username: str
    full_name: str
    password: str
    email:str