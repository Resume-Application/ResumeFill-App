from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.db import get_session
from app.models.company_models import CompanyJobPositionResponse, CompanyResponse, CreateCompanyJobPositionRequest, CreateCompanyRequest
from app.models.user_models import User, UserCreate, UserPublic
from app.core.security import hash_password, TokenResponse, create_access_token, verify_password
from app.routers.users import get_current_user
from app.services.company_services import create_job_posting, find_company_with_name, create_company, find_job_position_with_id, get_company_by_id, get_company_by_id, get_company_by_name, transform_company_to_response, transform_job_position_to_response
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/company/create", response_model=CompanyResponse)
async def create_company_route(
    current_user: Annotated[User, Depends(get_current_user)],
    companyRequest : CreateCompanyRequest,
    session : SessionDep
):
    '''
    Creates a new company.
    
    :param current_user: Description
    :type current_user: Annotated[User, Depends(get_current_user)]
    :param companyRequest: Description
    :type companyRequest: CreateCompanyRequest
    :param session: Description
    :type session: SessionDep
    '''

    logger.warning(f"Authentication for create_company_route not implemented")
    try: 
        company = create_company(session, companyRequest)
        companyResponse = transform_company_to_response(company)
        return companyResponse
    except ValueError as ve:
        logger.error(f"Failed to create company: {ve}")
        raise HTTPException(status_code=500, detail="Failed to create company")

@router.post("/company/job_posting/create", response_model=CompanyJobPositionResponse)
async def create_job_posting_route(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
    job_posting: CreateCompanyJobPositionRequest
):
    '''
    Docstring for create_job_posting_route
    
    :param form_data: Description
    :type form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    :param session: Description
    :type session: SessionDep
    :param job_posting: Description
    :type job_posting: CreateCompanyJobPositionRequest
    '''
    logger.warning(f"Authentication for create_job_posting_route not implemented")
    try:
        job_position = create_job_posting(session, job_posting)
        return transform_job_position_to_response(job_position)
    except ValueError as ve:
        logger.error(f"Failed to create job posting: {ve}")
        raise HTTPException(status_code=500, detail="Failed to create job posting")


@router.get("/company/{id}", response_model=CompanyResponse)
async def get_company_route(
    id: int,
    session : SessionDep
):
    try:
        company = get_company_by_id(session, id)
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")
        companyResponse = transform_company_to_response(company)
        return companyResponse
    except ValueError as ve:
        logger.error(f"Failed to get company: {ve}")
        raise HTTPException(status_code=500, detail="Failed to get company")
    
    
    
@router.get("/company/job_posting/{id}", response_model=CompanyJobPositionResponse)
async def get_job_posting_route(
    id: int,
    session : SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        job_posting = find_job_position_with_id(session, id)
        if job_posting is None:
            raise HTTPException(status_code=404, detail="Job posting not found")
        jobPostingResponse = transform_job_position_to_response(job_posting)
        return jobPostingResponse
    except ValueError as ve:
        logger.error(f"Failed to get job posting: {ve}")
        raise HTTPException(status_code=500, detail="Failed to get job posting")
    