from pydantic import ValidationError
from requests import Session
from app.core.db import get_session
from app.models.application_models import Application, ApplicationForm, ApplicationQuestionResponse, ApplicationResponse, ApplicationQuestionRequest, CreateApplicationRequest
from app.dependencies.auth_dependencies import get_current_user
from app.models.user_models import User
from typing import Annotated
from fastapi import Depends

from app.services.company_services import find_job_posting_with_url
from app.services.user_services import find_user_with_id
SessionDep = Annotated[Session, Depends(get_session)]

def create_applicationForm(session: SessionDep, application : Application, questionReq : ApplicationQuestionRequest, updateSession = True) -> ApplicationForm:
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


    if (updateSession):
        session.add(applicationForm)
        session.commit()

    return applicationForm

def create_application(session: SessionDep, 
                       request: CreateApplicationRequest, 
                       user_id: int) -> Application:
    '''
    Docstring for create_application
    
    :param request: Description
    :type request: CreateApplicationRequest
    :return: Description
    :rtype: ApplicationResponse
    '''
    try:
        request = CreateApplicationRequest.model_validate(request)
    except ValidationError as e:
        # item is NOT a valid CreateApplicationRequest
        raise ValueError(f"Invalid request data: {e}")

    # assert user_id exists
    user = find_user_with_id(session, user_id)
    if not user:
        raise ValueError("The user with this id does not exist in the system")
    # assert job with url exists exists

    job_position = find_job_posting_with_url(session, request.jobform_url)

    if not job_position:
        raise ValueError("The job position with this url does not exist in the system")
    

    application = Application(
        user_id = request.user_id,
        jobposition_id = job_position.id
    )
    session.add(application)
    session.flush()

    for questionReq in request.responses:
        try:
            questionReq = ApplicationQuestionRequest.model_validate(questionReq)
        except ValidationError as e:
            # item is NOT a valid ApplicationQuestionRequest
            raise ValueError(f"Invalid question/answer data: {e}")
        
        applicationForm = create_applicationForm(session, application, questionReq, updateSession=False)
        session.add(applicationForm)

    session.commit()

    return application

def get_application(session: SessionDep, id: int) -> Application | None:
    '''
    Docstring for get_application
    
    :param id: Description
    :type id: str
    :return: Description
    :rtype: ApplicationResponse | None
    '''

    application = session.query(Application).filter(Application.id == id).first()
    if not application:
        return None

    return application

def transform_application_to_response(session: SessionDep, application: Application) -> ApplicationResponse:
    '''
    Docstring for transform_application_to_response
    
    :param application: Description
    :type application: Application
    :return: Description
    :rtype: ApplicationResponse
    '''
    if isinstance(application, Application) == False:
        raise TypeError(
            f"application must be Application, got {type(application).__name__}"
        )

    applicationForms = session.query(ApplicationForm).filter(ApplicationForm.application_id == application.id).all()
    responses = []
    for form in applicationForms:
        question_response = ApplicationQuestionResponse(
            form_question = form.question_id,
            form_response = form.response,
            form_type = form.form_type
        )
        responses.append(question_response)

    applicationResponse = ApplicationResponse(
        user_id = application.user_id,
        jobposition_id = application.jobposition_id,
        responses = responses
    )

    return applicationResponse