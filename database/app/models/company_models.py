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

class CompanyJobPosition(SQLModel, table=True):
    '''
    Defines a job posting for a company
    '''
    id: int | None = Field(default=None, primary_key=True)
    company_id : int = Field(foreign_key="company.id", index=True)
    title : str
    location: str | None = None
    work_type: str | None = None  # e.g., remote, onsite, hybrid
    url : str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
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
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

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
    title : str
    company: str
    location: str | None = None
    work_type: str | None = None  # e.g., remote, onsite, hybrid
    url : str
    role_description: str = "full time" # full time, parttime, internship, contract

    low_pay_range : int | None = None
    high_pay_range : int | None = None
    form_questions: list[str]
    

class CompanyResponse(BaseModel):
    '''
    Response model for returning a company
    '''
    id: int
    name: str
    description: str | None = None
class CompanyJobPositionResponse(BaseModel):
    id : int
    title : str
    location: str
    url: str
    work_type: str
    role_description: str
    low_pay_range : int | None = None
    high_pay_range : int | None = None
