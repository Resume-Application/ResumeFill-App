from sqlmodel import Field, SQLModel
from datetime import datetime, timezone

class FormBase(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    question: str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    last_accessed : datetime