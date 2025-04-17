from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    # DATABASE_URL: str = "sqlite:///./cram_quest.db"  # Change to PostgreSQL if needed
    DATABASE_URL: str = f"postgresql+asyncpg://neondb_owner:{os.getenv('NEONDB_PASSWORD')}@ep-orange-mode-a13k4k1w-pooler.ap-southeast-1.aws.neon.tech/neondb?ssl=require" 

    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")  # Fallback in case .env is missing
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY", "default_secret_key")  # Fallback in case .env is missing
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))

    class Config:
        extra = "allow"
        env_file = ".env"  # Load environment variables
        

settings = Settings()
