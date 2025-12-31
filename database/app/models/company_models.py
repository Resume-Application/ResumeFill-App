from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


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
    application_id: int = Field(foreign_key="application.id", index=True)
    url : str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
        
