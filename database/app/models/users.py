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

class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str
    email:str

class UserPublic(UserBase):
    profile_img : str = "Default.png"

class UserLogin(BaseModel):
    '''Credentials for logging in'''
    username :str
    password:str