from datetime import datetime, timezone
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class CompanyJobPosition(SQLModel, table=True):
    '''
    Defines a job position for a company
    '''
    id: int | None = Field(default=None, primary_key=True)
    company_id : int = Field(foreign_key="company.id", index=True)
    title : str = Field(index=True)
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
    form_type : str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

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

class CompanyJobPositionResponse(BaseModel):
    id : int
    title : str
    location: str
    url: str
    work_type: str
    role_description: str
    low_pay_range : int | None = None
    high_pay_range : int | None = None