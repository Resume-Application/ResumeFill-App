from app.models.company_models import Company, CompanyResponse, CreateCompanyRequest
from app.models.job_position_models import CompanyJobForm, CompanyJobPosition
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
