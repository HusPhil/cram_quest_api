from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core.database import get_session
from app.core.auth import create_access_token
from app.crud.user_crud import crud_read_user_by_username
from app.core.security import Security

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    
    user = crud_read_user_by_username(session, username=form_data.username)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not Security.verify_hash(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
