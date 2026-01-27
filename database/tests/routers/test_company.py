from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.core.db import get_session
from sqlmodel.pool import StaticPool  
import pytest

from app.models.company_models import CompanyResponse
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

@pytest.fixture
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

def test_create_company(client: TestClient, auth_headers):
    payload = {
        "name": "Test Company",
        "description": "A company for testing"
    }

    response = client.post("/company/create", 
                           json=payload, 
                           headers=auth_headers)
    assert response.status_code == 200
    
def test_get_company(client: TestClient, auth_headers):
    payload = {
        "name": "Test Company",
        "description": "A company for testing"
    }
    response = client.post("/company/create", 
                           json=payload, 
                           headers=auth_headers)
    
    assert response.status_code == 200
    companyResp = CompanyResponse.model_validate(response.json())
    
    getResponse = client.get(f"/company/{companyResp.id}")

    assert getResponse.status_code == 200
    data = CompanyResponse.model_validate(getResponse.json())
    assert data.id == companyResp.id
    assert data.name == "Test Company"

def test_get_company_not_exist(client: TestClient):
    getResponse = client.get(f"/company/500")
    assert getResponse.status_code == 404
