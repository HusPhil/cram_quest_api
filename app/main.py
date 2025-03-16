from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import create_db_and_tables
from app.api.v1.endpoints import user_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Run database initialization
    yield  # Let the app run
    # Cleanup (if needed) goes here

app = FastAPI(title="CramQuest API", version="1.0.0")

@app.get('/')
async def root():
    return {"message": "Server is running!"}

app.include_router(user_routes.router, prefix="/users", tags=["users"])
