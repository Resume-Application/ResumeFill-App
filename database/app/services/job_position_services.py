from typing import Annotated, List
from sqlmodel import Session, select
from app.core.db import get_session
from fastapi import Depends
import logging
from app.models.company_models import Company
from app.models.job_position_models import CompanyJobForm, CompanyJobPositionResponse, CompanyJobPosition, CreateCompanyJobPositionRequest
from app.services.company_services import get_company_by_name   
logger = logging.getLogger(__name__)
SessionDep = Annotated[Session, Depends(get_session)]

def get_jobposition_by_company_and_title(session : SessionDep, company : Company, title : str) -> CompanyJobPosition | None:
    return session.exec(
        select(CompanyJobPosition).where(
            CompanyJobPosition.title == title,
            CompanyJobPosition.company_id == company.id
        )
    ).first()

def find_job_position_with_id(session : SessionDep, id : int) -> CompanyJobPosition | None:
    '''
    Finds a job posting with a specific id.
    
    :param session: Description
    :type session: SessionDep
    :param id: Description
    :type id: int
    :return: Description
    :rtype: CompanyJobPosition | None
    '''
    return session.exec(select(CompanyJobPosition).where(CompanyJobPosition.id == id)).first()

def find_jobform_with_id(session : SessionDep, id : int) -> CompanyJobForm | None:
    '''
    Finds a job form with a specific id.
    
    :param session: Description
    :type session: SessionDep
    :param id: Description
    :type id: int
    :return: Description
    :rtype: CompanyJobPosition | None
    '''
    return session.exec(select(CompanyJobForm).where(CompanyJobForm.id == id)).first()



def create_job_position(session : SessionDep, job_position : CreateCompanyJobPositionRequest) -> CompanyJobPosition | None:
    '''
    Creates a new job posting for a company. Raises an error if a job posting with the url exists.
    
    :param session: FastAPI session
    :type session: SessionDep
    :param url: Job position URL
    :return: Created job position
    '''

    if not isinstance(job_position, CreateCompanyJobPositionRequest):
        logger.error(f"Invalid job posting data: {job_position}")
        raise ValueError("Invalid job posting data provided")
    
    company = get_company_by_name(session, job_position.company)
    if company is None:
        logger.error(f"Company not found for job posting: {job_position.company}")
        raise ValueError("The specified company does not exist")
    

    try:
        companyPosition = CompanyJobPosition(
            title = job_position.title,
            url= job_position.url,
            company_id = company.id,
            location= job_position.location,
            work_type= job_position.work_type,
            role_description= job_position.role_description,
            low_pay_range= job_position.low_pay_range,
            high_pay_range= job_position.high_pay_range
        )
        session.add(companyPosition)
        session.flush()
        position_id = companyPosition.id

        for question in job_position.form_questions:
            job_form = CompanyJobForm(
                jobposition_id=position_id,
                question=question,
                form_type="text"
            )
            session.add(job_form)

        session.commit()
    except Exception as e:
        logger.error(f"Unexpected error {e}")
        raise ValueError(f"Unexpected error {e} while creating user")
    
    return companyPosition


def transform_job_position_to_response(job_position: CompanyJobPosition) -> CompanyJobPositionResponse:
    '''
    Transforms a CompanyJobPosition model to a CompanyJobPositionResponse model.
    
    :param job_position: CompanyJobPosition model
    :type job_position: CompanyJobPosition
    :return: CompanyJobPositionResponse model
    :rtype: CompanyJobPositionResponse
    '''

    return CompanyJobPositionResponse(
        id = job_position.id,
        title = job_position.title,
        location = job_position.location,
        url = job_position.url,
        work_type = job_position.work_type,
        role_description = job_position.role_description,
        low_pay_range = job_position.low_pay_range,
        high_pay_range = job_position.high_pay_range
    )