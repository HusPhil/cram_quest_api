from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.user_schema import UserCreate, UserRead
from app.crud.user_crud import create_user, get_user, get_all_users

router = APIRouter()

@router.post("/", response_model=UserCreate)
def create_user(username: str, email: str, password: str, session: Session = Depends(get_session)):
    return create_user(session, username, email, password)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):

    user = get_user(session, user_id)

    if not user:
        return {"error": "User not found."}

    return user

@router.get("/all", response_model=list[UserRead])
def read_all_users(session: Session = Depends(get_session)):
    return get_all_users(session)
