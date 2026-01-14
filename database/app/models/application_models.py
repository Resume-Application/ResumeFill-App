from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Application(SQLModel, table=True):
    """
    Defines an application for a user for a job.
    """
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True)
    jobposition_id: int = Field(foreign_key="companyjobposition.id", index=True)

    date_created: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class ApplicationForm(SQLModel, table=True):
    '''
    Defines a response to a question in an application.
    '''
    id: int | None = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    question_id: int = Field(foreign_key="companyjobform.id", index=True)
    response: str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

class ApplicationQuestionRequest(BaseModel):
    '''
    Request model for constructing a question/answer in an application
    '''
    form_question : str
    form_response : str
    form_type : str

class CreateApplicationRequest(BaseModel):
    '''
    Request model for creating an application
    '''
    user_id: int
    jobform_url : str
    responses: dict[str, ApplicationQuestionRequest] 

class ApplicationQuestionResponse(BaseModel):
    '''
    Response model for returning a question/answer in an application
    '''
    form_question : str
    form_response : str
    form_type : str

class ApplicationResponse(BaseModel):
    '''
    Response model for returning an a complete application
    '''
    user_id: int
    jobposition_id: int
    responses: dict[str, ApplicationQuestionResponse] 