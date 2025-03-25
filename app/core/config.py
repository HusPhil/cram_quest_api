from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./cram_quest.db"  # Change to PostgreSQL if needed
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")  # Fallback in case .env is missing
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    class Config:
        env_file = ".env"  # Load environment variables
        

settings = Settings()
