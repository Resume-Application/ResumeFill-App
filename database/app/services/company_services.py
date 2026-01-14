from app.models.company_models import Company, CompanyJobForm, CompanyJobPosition, CreateCompanyRequest, CreateCompanyJobPositionRequest
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

def find_job_posting_with_url(session : SessionDep, url : str) -> CompanyJobPosition | None:
    return session.exec(select(CompanyJobPosition).where(CompanyJobPosition.url == url)).first() 

def create_job_posting(session : SessionDep, url : str, form_questions : list[str]) -> CompanyJobPosition | None:
    '''
    Creates a new job posting for a company. Raises an error if a job posting with the url exists.
    
    :param session: FastAPI session
    :type session: SessionDep
    :param url: Job position URL
    :return: Created job position
    '''
    job_posting = find_job_posting_with_url(session, url)
    if job_posting:
        logger.error(f"Attempted to create job posting with existing url: {url}")
        raise ValueError("The job posting with this url already exists in the system")
    
    try:
        companyPosition = CompanyJobPosition(
            url= url
        )
        session.add(companyPosition)
        session.flush()
        position_id = companyPosition.id

        for question in form_questions:
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