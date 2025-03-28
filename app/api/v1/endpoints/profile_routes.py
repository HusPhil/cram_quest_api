from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.profile_schema import ProfileCreate, ProfileRead, ProfileUpdate
from app.crud.profile_crud import crud_create_profile, crud_read_profile, crud_read_all_profiles, crud_update_profile

router = APIRouter()

@router.post("/{player_id}", response_model=ProfileRead)
async def create_profile(player_id: int, profile_create: ProfileCreate, session: AsyncSession = Depends(get_session)):
    return await crud_create_profile(session, player_id, profile_create)

@router.get("/{profile_id}", response_model=ProfileRead)
async def read_profile(profile_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_read_profile(session, profile_id)

@router.get("/", response_model=list[ProfileRead])
async def read_all_profiles(session: AsyncSession = Depends(get_session)):
    return await crud_read_all_profiles(session)

@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_profile(profile_id: int, profile_update: ProfileUpdate, session: AsyncSession = Depends(get_session)):
    return await crud_update_profile(session, profile_id, profile_update)