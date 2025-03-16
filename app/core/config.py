from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./cram_quest.db"  # Change to PostgreSQL if needed

    class Config:
        env_file = ".env"  # Load environment variables

settings = Settings()
