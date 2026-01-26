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

@pytest.fixture(name="client_with_user")
def client_with_user_fixture(client: TestClient, session: Session):
    user_in = UserCreate(
        email="test@example.com",
        password="password123",
    )

    user = create_user(session=session, user_create=user_in)

    yield client
def create_test_application(session: Session, client: TestClient):
    # Create a test user
    