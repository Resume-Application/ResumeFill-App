from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlmodel import Session
from app.core.db import get_session
from app.dependencies.auth_dependencies import get_current_user
from app.models.user_models import UserPublic
from app.models.application_models import ApplicationResponse, CreateApplicationRequest
from app.models.user_models import User
import logging

from app.services.application_services import create_application, get_application, transform_application_to_response
router = APIRouter()
logger = logging.getLogger(__name__)
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/application/create", response_model=ApplicationResponse)
def create_application_route(payload: CreateApplicationRequest,
                       current_user: Annotated[User, Depends(get_current_user)],
                       session: SessionDep  
    ):
    '''
    Docstring for create_application endpoint

    :param payload: Description
    :type payload: CreateApplicationRequest
    :return: Description
    :rtype: ApplicationResponse
    '''

    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        application = create_application(session, payload, current_user.id)

        return transform_application_to_response(session, application)
    except ValueError as e:
        logger.error(f"Failed to create application: {e}")
        raise HTTPException(status_code=400, detail="Failed to create application")
    

@router.get("/application/{id}", response_model=ApplicationResponse)
def get_application_route(
    id: int, 
    current_user: Annotated[User, Depends(get_current_user)],
    session : SessionDep):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    application = get_application(session, id)
    
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return transform_application_to_response(session,application)
    
