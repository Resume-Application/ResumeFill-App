from sqlmodel import Session, create_engine, select, SQLModel

from app.core.config import settings

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def init_db() -> None:
    # Import all models so that SQLModel knows about them
    from app import models
    SQLModel.metadata.create_all(engine)