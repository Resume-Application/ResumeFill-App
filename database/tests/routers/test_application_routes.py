import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.core.security import create_access_token
from app.models.application_models import ApplicationResponse
from app.models.company_models import CompanyResponse
from app.models.user_models import User
from app.services.user_services import create_user, UserCreate
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
 
@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session
    app.dependency_overrides[get_session] = get_session_override  
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()  

@pytest.fixture(name="auth_headers")
def auth_headers(client: TestClient):
    # Register
    register_response = client.post(
        "/auth/register",
        json={
            "username": "Deadpool",
            "full_name": "Dive Wilson",
            "password": "DeadpoolsPassword",
            "email": "deadpool@gmail.com",
        },
    )
    assert register_response.status_code in (200, 201)

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "Deadpool",
            "password": "DeadpoolsPassword",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="populated_client")
def populated_client(client : TestClient, auth_headers):
    payload = {
        "name": "Test Company",
        "description": "A company for testing"
    }
    response = client.post("/company/create", 
                           json=payload, 
                           headers=auth_headers)
    companyResp = CompanyResponse.model_validate(response.json())
    payload = {
        "title": "Software Engineer",
        "company": "Test Company",
        "location": "San Francisco, CA",
        "work_type": "onsite",
        "url": "fake.com/apply",
        "role_description": "full time",
        "low_pay_range": 80000,
        "high_pay_range": 120000,
        "form_questions": ["What is your experience?", 
                           "Why do you want this job?",
                           "What are your strengths?"],
    }

    response = client.post("/job_position/create",
                            json=payload,
                            headers=auth_headers)
    
    return client

def test_create_application(populated_client: TestClient, auth_headers):
    payload = {
        "company" : "Test Company",
        "title" : "Software Engineer",
        "responses" : [
            {
                "form_question" : "What is your experience?",
                "form_response" : "I have 5 years of experience.",
                "form_type" : "text"
            },
            {
                "form_question" : "Why do you want this job?",
                "form_response" : "Because I love coding.",
                "form_type" : "text"
            },
            {
                "form_question" : "What are your strengths?",
                "form_response" : "Problem solving and teamwork.",
                "form_type" : "text"
            }
        ]
    }

    response = populated_client.post("/application/create",
                           json=payload,
                           headers=auth_headers)
    
    assert response.status_code == 200
def test_create_application_missing_auth(populated_client: TestClient, auth_headers):
    payload = {
        "company" : "Test Company",
        "title" : "Software Engineer",
        "responses" : [
            {
                "form_question" : "What is your experience?",
                "form_response" : "I have 5 years of experience.",
                "form_type" : "text"
            },
            {
                "form_question" : "Why do you want this job?",
                "form_response" : "Because I love coding.",
                "form_type" : "text"
            },
            {
                "form_question" : "What are your strengths?",
                "form_response" : "Problem solving and teamwork.",
                "form_type" : "text"
            }
        ]
    }
    response = populated_client.post("/application/create",
                           json=payload)
    
    assert response.status_code == 401

def test_create_malformed_application(populated_client: TestClient, auth_headers):
    payload = {
        "company" : "Test Company",
        "title" : "Software Engineer",
        "responses" : [
            {
                "form_question" : "What is your experience?",
                "form_response" : "I have 5 years of experience.",
                "form_type" : "text"
            },
            {
                "form_question" : "This is a fake question?",
                "form_response" : "Because I love coding.",
                "form_type" : "text"
            },
            {
                "form_question" : "This is a fake question.",
                "form_response" : "Problem solving and teamwork.",
                "form_type" : "text"
            }
        ]
    }

    response = populated_client.post("/application/create",
                           json=payload,
                           headers=auth_headers)
    
    assert response.status_code == 400

def test_get_nonexistent_application(populated_client: TestClient, auth_headers):
    response = populated_client.get(f"/application/500",
                                    headers=auth_headers)
    
    assert response.status_code == 404
def test_get_application(populated_client: TestClient, auth_headers):
    payload = {
        "company" : "Test Company",
        "title" : "Software Engineer",
        "responses" : [
            {
                "form_question" : "What is your experience?",
                "form_response" : "I have 5 years of experience.",
                "form_type" : "text"
            },
            {
                "form_question" : "Why do you want this job?",
                "form_response" : "Because I love coding.",
                "form_type" : "text"
            },
            {
                "form_question" : "What are your strengths?",
                "form_response" : "Problem solving and teamwork.",
                "form_type" : "text"
            }
        ]
    }

    response = populated_client.post("/application/create",
                           json=payload,
                           headers=auth_headers)
    data = ApplicationResponse.model_validate(response.json())
    assert response.status_code == 200
    application_id = data.application_id
    assert application_id is not None

    response = populated_client.get(f"/application/{application_id}",
                                    headers=auth_headers)
    assert response.status_code == 200


