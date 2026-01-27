
import logging
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlmodel import Session
from typing_extensions import Annotated

from app.core.db import get_session
from app.models.job_position_models import CompanyJobPositionResponse, CreateCompanyJobPositionRequest
from app.models.user_models import User
from app.routers.users_routes import get_current_user
from app.services.job_position_services import create_job_position, find_job_position_with_id, transform_job_position_to_response


logger = logging.getLogger(__name__)

router = APIRouter()

    
SessionDep = Annotated[Session, Depends(get_session)]
@router.post("/job_position/create", response_model=CompanyJobPositionResponse)
async def create_job_position_route(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
    job_position: CreateCompanyJobPositionRequest
):
    '''
    Docstring for create_job_position_route
    
    :param form_data: Description
    :type form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    :param session: Description
    :type session: SessionDep
    :param job_position: Description
    :type job_position: CreateCompanyJobPositionRequest
    '''
    logger.warning(f"Authentication for create_job_position_route not implemented")
    try:
        job_position = create_job_position(session, job_position)
        return transform_job_position_to_response(job_position)
    except ValueError as ve:
        logger.error(f"Failed to create job posting: {ve}")
        raise HTTPException(status_code=500, detail="Failed to create job posting")


@router.get("/job_position/{id}", response_model=CompanyJobPositionResponse)
async def get_job_position_route(
    id: int,
    session : SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        job_position = find_job_position_with_id(session, id)
        if job_position is None:
            raise HTTPException(status_code=404, detail="Job position not found")
        jobPositionResponse = transform_job_position_to_response(job_position)
        return jobPositionResponse
    except ValueError as ve:
        logger.error(f"Failed to get job position: {ve}")
        raise HTTPException(status_code=500, detail="Failed to get job position")
    