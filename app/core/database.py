from sqlmodel import SQLModel, create_engine, Session, text
from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        session.exec(text("PRAGMA foreign_keys = ON;"))
        yield session
    

# Function to create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
