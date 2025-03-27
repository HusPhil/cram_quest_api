from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import create_db_and_tables
from app.api.v1.endpoints import (
    user_routes, player_routes, 
    auth_routes, test_routes, 
    profile_routes, subject_routes, 
    study_session_routes, quest_routes
)
app = FastAPI(title="CramQuest API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    print("Starting up cramquest...")
    create_db_and_tables()  # Automatically create missing tables

@app.get('/')
async def root():
    return {"message": "Server is running!"}

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(player_routes.router, prefix="/players", tags=["players"])
app.include_router(profile_routes.router, prefix="/profiles", tags=["profiles"])
app.include_router(subject_routes.router, prefix="/subjects", tags=["subjects"])
app.include_router(study_session_routes.router, prefix="/study_sessions", tags=["study_sessions"])
app.include_router(quest_routes.router, prefix="/quests", tags=["quests"])


app.include_router(test_routes.router, prefix="/tests", tags=["tests"])
