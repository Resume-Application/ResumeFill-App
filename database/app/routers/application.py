from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.dependencies.auth_dependencies import get_current_user
from app.models import UserPublic
from app.models.application_models import ApplicationResponse, CreateApplicationRequest
from app.models.user_models import User

router = APIRouter()

@router.middle

@router.post("/application/create", response_model=ApplicationResponse)
def create_application(payload: CreateApplicationRequest,
                       current_user: Annotated[User, Depends(get_current_user)]
    ):
    '''
    Docstring for create_application endpoint

    :param payload: Description
    :type payload: CreateApplicationRequest
    :return: Description
    :rtype: ApplicationResponse
    '''
    
    # check if a jobposition with url exists. otherwise, create it

    # create the application


    

    

@router.get("/application/{id}", response_model=ApplicationResponse)
def get_application(id: str):
    
@router.delete("/application/{id}")
def delete_application(
    id: str,
    _: str = Depends(s),
):
    

@router.get("/responses/{id}")
def get_response(id: str):
   
