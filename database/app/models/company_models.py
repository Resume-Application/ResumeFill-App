from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from pydantic import BaseModel

class Company(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CreateCompanyRequest(BaseModel):
    '''
    Request model for creating a company
    '''
    name: str
    description: str | None = None
    

class CompanyResponse(BaseModel):
    '''
    Response model for returning a company
    '''
    id: int
    name: str
    description: str | None = None

