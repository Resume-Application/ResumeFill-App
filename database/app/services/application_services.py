from pydantic import ValidationError
from requests import Session
from app.core.db import get_session
from app.models.application_models import Application, ApplicationForm, ApplicationFormRequest, ApplicationFormResponse, ApplicationResponse, CreateApplicationRequest
from app.dependencies.auth_dependencies import get_current_user
from app.models.job_position_models import CompanyJobForm
from app.models.user_models import User
from typing import Annotated, List
from fastapi import Depends

from app.services.company_services import find_company_with_name
from app.services.job_position_services import find_jobform_with_id, get_jobposition_by_company_and_title
from app.services.user_services import find_user_with_id
SessionDep = Annotated[Session, Depends(get_session)]

def create_applicationForm(session: SessionDep, 
                           application : Application,
                           companyJobForm : CompanyJobForm, 
                           questionReq : ApplicationFormRequest, 
                           updateSession = True) -> ApplicationForm:
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
        question_id = companyJobForm.id,
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

    company = find_company_with_name(session, request.company)
    if not company:
        raise ValueError("The company with this name does not exist in the system")
    job_position = get_jobposition_by_company_and_title(session, company, request.title)
    if not job_position:
        raise ValueError("The job position with this url does not exist in the system")
    

    application = Application(
        user_id = user_id,
        jobposition_id = job_position.id
    )
    session.add(application)
    session.flush()

    jobforms = session.query(CompanyJobForm).filter(CompanyJobForm.jobposition_id == job_position.id).all()

    for questionReq in request.responses:
        try:
            questionReq = ApplicationFormRequest.model_validate(questionReq)
        except ValidationError as e:
            # item is NOT a valid ApplicationFormRequest
            raise ValueError(f"Invalid question/answer data: {e}")
        added = False
        for jobform in jobforms:
            if jobform.question == questionReq.form_question:
                applicationForm = create_applicationForm(
                    session,
                    application,
                    jobform,
                    questionReq,
                    updateSession=False
                )
                session.add(applicationForm)
                added = True
                break
        if not added:
            raise ValueError(f"Question not found in job forms: {questionReq.form_question}")
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

    applicationForms : List[ApplicationForm] = session.query(ApplicationForm).filter(ApplicationForm.application_id == application.id).all()
    responses = []
    for form in applicationForms:
        formQuestion = find_jobform_with_id(session, form.question_id)

        question_response = ApplicationFormResponse(
            form_question = formQuestion.question,
            form_response = form.response,
        )
        responses.append(question_response)

    applicationResponse = ApplicationResponse(
        application_id = application.id,
        jobposition_id = application.jobposition_id,
        responses = responses
    )

    return applicationResponse

def count_user_applications(session: SessionDep, user_id: int) -> int:
    '''
    Counts the number of applications submitted by a user.
    
    :param session: Database session
    :type session: SessionDep
    :param user_id: ID of the user
    :type user_id: int
    :return: Number of applications submitted by the user
    :rtype: int
    '''
    application_count = session.query(Application).filter(Application.user_id == user_id).count()
    return application_count