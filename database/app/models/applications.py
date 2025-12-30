from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Application(SQLModel, table=True):
    '''
    Defines an application for a user for a job.
    '''
    id: int | None = Field(default=None, primary_key=True)