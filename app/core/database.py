from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Import models so they are registered
from app.models.user_model import User
from app.models.player_model import Player
from app.models.profile_model import Profile
from app.models.subject_model import Subject
from app.models.study_session_model import StudySession
from app.models.quest_model import Quest

# ✅ Create async database engine
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
    future=True,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800
)

AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ Create async session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# ✅ Dependency to get an async session
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# ✅ Function to create tables asynchronously
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

