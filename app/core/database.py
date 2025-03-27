from sqlmodel import SQLModel, create_engine, Session, text
from app.core.config import settings
from app.models.user_model import User
from app.models.player_model import Player
from app.models.profile_model import Profile
from app.models.subject_model import Subject
from app.models.study_session_model import StudySession
from app.models.quest_model import Quest

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
