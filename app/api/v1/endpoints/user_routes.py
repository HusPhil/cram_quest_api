from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.user_schema import UserCreate, UserRead
from app.crud.user_crud import create_user, get_users

router = APIRouter()

@router.post("/", response_model=UserCreate)
def create_user_api(username: str, email: str, password: str, session: Session = Depends(get_session)):
    return create_user(session, username, email, password)

@router.get("/", response_model=list[UserRead])
def read_users_api(session: Session = Depends(get_session)):
    return get_users(session)
