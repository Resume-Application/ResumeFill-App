from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from pydantic import BaseModel

class Company(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CompanyJobPosition(SQLModel, table=True):
    '''
    Defines a job posting for a company
    '''
    id: int | None = Field(default=None, primary_key=True)
    title : str
    location: str
    work_type: str  # e.g., remote, onsite, hybrid
    url : str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    role_description: str = "full time" # full time, parttime, internship, contract

    low_pay_range : int | None = None
    high_pay_range : int | None = None

class CompanyJobForm(SQLModel, table=True):
    '''
    Defines a form belonging to a job position
    '''
    id: int | None = Field(default=None, primary_key=True)
    jobposition_id: int = Field(foreign_key="companyjobposition.id", index=True)
    question : str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


class CreateCompanyRequest(BaseModel):
    '''
    Request model for creating a company
    '''
    name: str
    description: str | None = None

class CreateCompanyJobPositionRequest(BaseModel):
    '''
    Request model for creating a job position
    '''
    url : str
    form_questions : list[str]
