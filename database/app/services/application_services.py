from requests import Session
from app.core.db import get_session
from app.models.application_models import Application, ApplicationForm, ApplicationResponse, ApplicationQuestionRequest, CreateApplicationRequest
from app.dependencies.auth_dependencies import get_current_user
from app.models.user_models import User
from typing import Annotated
from fastapi import Depends

from app.services.company_services import find_job_posting_with_url
from app.services.user_services import find_user_with_id
SessionDep = Annotated[Session, Depends(get_session)]

def create_applicationForm(session: SessionDep, application : Application, questionReq : ApplicationQuestionRequest) -> ApplicationForm:
    '''
    Creates a response to a question in an application.
    
    :param application: Description
    :type application: Application
    :param questionReq: Description
    :type questionReq: ApplicationQuestionRequest
    :return: Description
    :rtype: ApplicationForm
    '''

    applicationForm = ApplicationForm(
        user_id = application.user_id,
        application_id = application.id,
        
        response = questionReq.form_response
    )
    return applicationForm

def create_application(session: SessionDep, 
                       request: CreateApplicationRequest, 
                       user_id: int) -> ApplicationResponse:
    '''
    Docstring for create_application
    
    :param request: Description
    :type request: CreateApplicationRequest
    :return: Description
    :rtype: ApplicationResponse
    '''

    # assert user_id exists
    user = find_user_with_id(session, user_id)
    if not user:
        raise ValueError("The user with this id does not exist in the system")
    # assert job with url exists exists

    job_position = find_job_posting_with_url(session, request.jobform_url)

    if not job_position:
        raise ValueError("The job position with this url does not exist in the system")
    


