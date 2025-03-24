from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.user_schema import UserCreate, UserRead
from app.crud.user_crud import crud_create_user, crud_read_user, crud_read_all_users, crud_update_user
from app.core.auth import get_current_user
from typing import Optional

router = APIRouter()
 
@router.post("/create/user/", response_model=UserRead)
def create_user(username: str, email: str, password: str, session: Session = Depends(get_session)):
    return crud_create_user(session, username, email, password)

@router.put("/update/user/", response_model=UserRead)
def update_user(user_id: int, username: str = None, email: str = None, password: Optional[str] = None, session: Session = Depends(get_session)):
    return crud_update_user(session, user_id, username, email, password)

@router.get("/read/id/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    
    if current_user:
        print(current_user)

    user = crud_read_user(session, user_id)

    if not user:
        return {"error": "User not found."}

    return user

@router.get("/read/all", response_model=list[UserRead])
def read_all_users(session: Session = Depends(get_session)):
    return crud_read_all_users(session)


