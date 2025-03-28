from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.profile_schema import ProfileCreate, ProfileRead, ProfileUpdate
from app.crud.profile_crud import crud_create_profile, crud_read_profile, crud_read_all_profiles, crud_update_profile

router = APIRouter()

@router.post("/{player_id}")
def create_profile(player_id: int, profile: ProfileCreate, session: Session = Depends(get_session)):
    return crud_create_profile(session, player_id, profile.avatar_url, profile.bio, profile.mood)

@router.get("/{profile_id}", response_model=ProfileRead)
def read_profile(profile_id: int, session: Session = Depends(get_session)):
    return crud_read_profile(session, profile_id)

@router.get("/", response_model=list[ProfileRead])
def read_all_profiles(session: Session = Depends(get_session)):
    return crud_read_all_profiles(session)

@router.patch("/{profile_id}", response_model=ProfileRead)
def update_profile(profile_id: int, profile_update: ProfileUpdate, session: Session = Depends(get_session)):
    return crud_update_profile(session, profile_id, profile_update)