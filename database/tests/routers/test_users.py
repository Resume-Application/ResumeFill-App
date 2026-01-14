import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.core.security import create_access_token
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

def test_read_users_me(client: TestClient):
    # Create a user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "Deadpool",
            "full_name": "Dive Wilson",
            "password": "DeadpoolsPassword",
            "email": "deadpool@gmail.com"
        }
    )
    assert register_response.status_code == 200

    # Login with correct credentials
    login_response = client.post(
        "/auth/login",
        data={
            "username": "Deadpool",
            "password": "DeadpoolsPassword"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    print("TOKEN:", token)
    response = client.get("/user/profile", headers={"Authorization": f"Bearer {token}"})
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    assert response.status_code == 200
    assert response.json()["username"] == "Deadpool"

def test_read_users_me_unauthorized(client: TestClient):
    response = client.get("/user/profile")
    assert response.status_code == 401
