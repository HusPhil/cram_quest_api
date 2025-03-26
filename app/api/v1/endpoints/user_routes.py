from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.crud.user_crud import crud_create_user, crud_read_user_by_id, crud_read_all_users, crud_update_user, crud_delete_user
from app.core.auth import get_current_user
from typing import Optional

# router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])
router = APIRouter()
 
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return crud_create_user(session, user.username, user.email, user.password.get_secret_value())

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):

    return crud_update_user(session, user_id, user_update)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    return crud_read_user_by_id(session, user_id)

@router.get("/", response_model=list[UserRead])
def read_all_users(session: Session = Depends(get_session)):
    return crud_read_all_users(session)

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    return crud_delete_user(session, user_id)

