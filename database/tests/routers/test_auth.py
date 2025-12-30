from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app, get_session
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
    assert data["name"] == "Deadpool"
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
    assert data["name"] == "Deadpool"
    assert data["disabled"] == False

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
    assert data["name"] == "Deadpool"
    assert data["disabled"] == False

    dup_payload = payload.copy()
    dup_payload["username"] = "Gwenpool" 
    response2 = client.post("/auth/register", json=dup_payload)
    assert response2.status_code == 400

#def test_login_success(client):
    
#def test_login_wrong_password(client):
    
#def test_login_non_existent_user(client):