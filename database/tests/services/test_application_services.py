import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.models.company_models import CreateCompanyJobPositionRequest, CreateCompanyRequest
from app.services.application_services import create_application, CreateApplicationRequest
from app.services.user_services import create_user, UserCreate
from app.services.company_services import create_company
from sqlmodel.pool import StaticPool  
from app.core.db import get_session
from app.main import app

@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  
@pytest.fixture(name="populated_session"):
def populated_session_fixture(session: Session):  
    user_in = UserCreate(
        email="test123@testmail.com",
        full_name="Test Joe",
        password="securepassword",
        username="JoesAccount"
    )
    user = create_user(session=session, user_create=user_in)
    create_company = CreateCompanyRequest(
        name="Test Company",
        description="A test company for testing purposes"
    )
    company = create_company(session, create_company)

    company_jobposition_request = CreateCompanyJobPositionRequest(
        url="testcompany.com/job"
    )
    yield session



def test_create_application_base(session: Session):
    '''
    Docstring for test_create_application_base
    Creates an application with valid data 
    '''

    request = CreateApplicationRequest(
        user_id=1,
        jobform_url="https://example.com",
        responses=[]
    )

    application = create_application(session, request, 1)
    assert application is not None

def test_create_applicationForm_base():

def test_get_application_exists():
    '''
    Docstring for test_get_application_exists
    Retrieves an existing application by ID
    '''
def test_get_application_not_exists():
    '''
    Docstring for test_get_application_not_exists
    Attempts to retrieve a non-existing application by ID
    '''

def test_transform_application_to_response_base():
    '''
    Docstring for test_transform_application_to_response_base with usual data
    '''

def test_transform_application_to_response_malformed_application():
    '''
    Docstring for test_transform_application_to_response_malformed_application
    '''

