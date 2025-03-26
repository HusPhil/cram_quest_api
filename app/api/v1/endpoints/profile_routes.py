from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.profile_schema import ProfileCreate
from app.crud.profile_crud import crud_create_profile

router = APIRouter()

@router.post("/{player_id}")
def create_profile(player_id: int, profile: ProfileCreate, session: Session = Depends(get_session)):
    return crud_create_profile(session, player_id, profile.avatar_url, profile.bio, profile.mood)