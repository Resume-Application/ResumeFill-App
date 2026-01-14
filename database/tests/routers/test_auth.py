from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.core.db import get_session
from sqlmodel.pool import StaticPool  
import pytest

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

def test_register_user_success(client : TestClient):
    response = client.post(
        "/auth/register", json={"username": "Deadpool", 
                          "full_name": "Dive Wilson",
                          "password": "DeadpoolsPassword",
                          "email": "deadpool@gmail.com"}
    )
    data = response.json()
    assert response.status_code==200
    assert data["username"] == "Deadpool"
    assert data["disabled"] == False

def test_register_duplicate_username(client : TestClient):
    '''Ensures no duplicate usernames exist in the database '''
    payload = {
            "username": "Deadpool", 
            "full_name": "Wade Wilson",
            "password": "password123",
            "email": "deadpool@example.com"
        }
    response1 = client.post("/auth/register", json=payload)
    data = response1.json()
    assert response1.status_code==200

    dup_payload = payload.copy()
    dup_payload["email"] = "other_email@example.com" 
    response2 = client.post("/auth/register", json=dup_payload)
    assert response2.status_code == 400

def test_register_duplicate_email(client : TestClient):
    '''Ensures no duplicate emails exist in the database '''
    payload = {
            "username": "Deadpool", 
            "full_name": "Wade Wilson",
            "password": "password123",
            "email": "deadpool@example.com"
        }
    response1 = client.post("/auth/register", json=payload)
    data = response1.json()
    assert response1.status_code==200

    dup_payload = payload.copy()
    dup_payload["username"] = "Gwenpool" 
    response2 = client.post("/auth/register", json=dup_payload)
    assert response2.status_code == 400
def test_login_success(client: TestClient):
    # Register user
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
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_response.status_code == 200
    body = login_response.json()

    assert "access_token" in body
    assert "token_type" in body
    assert body["token_type"].lower() == "bearer"

def test_login_wrong_password(client: TestClient):
    # Ensure user exists
    client.post(
        "/auth/register",
        json={
            "username": "Deadpool2",
            "full_name": "Wade Wilson",
            "password": "CorrectPassword",
            "email": "deadpool2@gmail.com"
        }
    )

    # Attempt login with wrong password
    response = client.post(
        "/auth/login",
        data={
            "username": "Deadpool2",
            "password": "WrongPassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_non_existent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        data={
            "username": "NonExistentUser",
            "password": "DoesNotMatter"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"
