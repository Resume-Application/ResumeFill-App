from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Application(SQLModel, table=True):
    """
    Defines an application for a user for a job.
    """
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True)

    date_created: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class ApplicationResponse(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    question: str
    response: str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
        
