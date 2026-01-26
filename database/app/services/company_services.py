from app.models.company_models import Company, CompanyJobForm, CompanyJobPosition, CompanyJobPositionResponse, CompanyResponse, CreateCompanyRequest, CreateCompanyJobPositionRequest
from typing import Annotated, List
from sqlmodel import Session, select
from app.core.db import get_session
from fastapi import Depends
import logging
logger = logging.getLogger(__name__)
SessionDep = Annotated[Session, Depends(get_session)]

def find_company_with_name(session : SessionDep, name : str) -> Company | None:
    return session.exec(select(Company).where(Company.name == name)).first()

def create_company(session : SessionDep, company_in : CreateCompanyRequest) -> Company | None:
    '''
    Creates a new company in the database.
    
    :param session: FastAPI session
    :type session: SessionDep
    :param company_in: Company creation request
    :type company_in: CreateCompanyRequest
    :return: Created company
    '''
    try:
        company = Company(
            name= company_in.name,
            description=company_in.description
        )
        session.add(company)
        session.commit()
    except Exception as e:
        logger.error(f"Unexpected error {e}")
        raise ValueError(f"Unexpected error {e} while creating user")
    
    return company

def get_company_by_name(session : SessionDep, name : str) -> Company | None:
    return session.exec(select(Company).where(Company.name == name)).first()

def get_company_by_id(session : SessionDep, id : int) -> Company | None:
    return session.exec(select(Company).where(Company.id == id)).first()

def find_job_posting_with_url(session : SessionDep, url : str) -> CompanyJobPosition | None:
    '''
    Finds a job posting with a specific url.
    
    :param session: Description
    :type session: SessionDep
    :param url: Description
    :type url: str
    :return: Description
    :rtype: CompanyJobPosition | None
    '''
    return session.exec(select(CompanyJobPosition).where(CompanyJobPosition.url == url)).first() 

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

def create_job_posting(session : SessionDep, job_posting : CreateCompanyJobPositionRequest) -> CompanyJobPosition | None:
    '''
    Creates a new job posting for a company. Raises an error if a job posting with the url exists.
    
    :param session: FastAPI session
    :type session: SessionDep
    :param url: Job position URL
    :return: Created job position
    '''

    if not isinstance(job_posting, CreateCompanyJobPositionRequest):
        logger.error(f"Invalid job posting data: {job_posting}")
        raise ValueError("Invalid job posting data provided")

    existing_job = find_job_posting_with_url(session, job_posting.url)
    if existing_job:
        logger.error(f"Attempted to create job posting with existing url: {job_posting.url}")
        raise ValueError("The job posting with this url already exists in the system")
    company = get_company_by_name(session, job_posting.company)
    if company is None:
        logger.error(f"Company not found for job posting: {job_posting.company}")
        raise ValueError("The specified company does not exist")
    

    try:
        companyPosition = CompanyJobPosition(
            title = job_posting.title,
            url= job_posting.url,
            company_id = company.id,
            location= job_posting.location,
            work_type= job_posting.work_type,
            role_description= job_posting.role_description,
            low_pay_range= job_posting.low_pay_range,
            high_pay_range= job_posting.high_pay_range
        )
        session.add(companyPosition)
        session.flush()
        position_id = companyPosition.id

        for question in job_posting.form_questions:
            job_form = CompanyJobForm(
                jobposition_id=position_id,
                question=question
            )
            session.add(job_form)

        session.commit()
    except Exception as e:
        logger.error(f"Unexpected error {e}")
        raise ValueError(f"Unexpected error {e} while creating user")
    
    return companyPosition


def create_companyjobform(session: SessionDep, jobPosition: CompanyJobPosition, question: str) -> CompanyJobForm:
    '''
    Creates a form question for a job position.
    
    :param session: FastAPI session
    :type session: SessionDep
    :param jobPosition: Job position
    :type jobPosition: CompanyJobPosition
    :param question: Question text
    :type question: str
    :return: Created CompanyJobForm
    :rtype: CompanyJobForm
    '''
    companyJobForm = CompanyJobForm(
        jobposition_id = jobPosition.id,
        question = question
    )
    return companyJobForm

def query_jobform_question(session:SessionDep, question: str, company : Company):
    '''Search for a company with a specific question name'''
    company_id = company.id
    return session.exec(
        select(CompanyJobForm).where(
            CompanyJobForm.question == question,
            CompanyJobForm.jobposition_id == company_id
        )
    ).first()

def transform_company_to_response(company: Company) -> CompanyResponse:
    '''
    Transforms a Company model to a CreateCompanyRequest model.
    
    :param company: Company model
    :type company: Company
    :return: CreateCompanyRequest model
    :rtype: CreateCompanyRequest
    '''
    return CompanyResponse(
        id = company.id,
        name=company.name,
        description=company.description
    )

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