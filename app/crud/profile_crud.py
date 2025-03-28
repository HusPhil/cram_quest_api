from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import Player, Profile
from app.schemas.profile_schema import ProfileRead, ProfileUpdate, ProfileCreate
from app.crud.player_crud import PlayerNotFound
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError

class ProfileNotFound(HTTPException):
    def __init__(self, profile_id: int):
        super().__init__(status_code=404, detail=f"Profile {profile_id} not found")

class ProfileAlreadyExist(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=400, detail=f"Profile already exists for player: {player_id}")

async def crud_create_profile(session: AsyncSession, player_id: int, profile_create: ProfileCreate) -> ProfileRead:
    
    player, profile = await _get_player_and_profile_or_error(session, player_id)

    new_profile = Profile(
        player_id=player_id, 
        avatar_url=profile_create.avatar_url, 
        bio=profile_create.bio, 
        mood=profile_create.mood
    )

    try:
        session.add(new_profile)    
        await session.commit()
        await session.refresh(new_profile)

        return _serialize_profile(new_profile)
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise RuntimeError(f"Unexpected SQLAlchemyError while creating Profile: {str(e)}")
    except Exception as e:
        await session.rollback()
        raise RuntimeError(f"Unexpected error while creating Profile: {str(e)}")

async def crud_read_profile(session: AsyncSession, profile_id: int) -> ProfileRead:
    profile = await _get_profile_or_error(session, profile_id)
    return _serialize_profile(profile)

async def crud_read_all_profiles(session: AsyncSession) -> list[ProfileRead]:
    statement = (
        select(Profile)
        .options(joinedload(Profile.player))
    )

    result = await session.execute(statement)
    profiles = result.scalars().all()

    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found")

    profiles_with_users = [_serialize_profile(profile) for profile in profiles]

    return profiles_with_users

async def crud_update_profile(session: AsyncSession, profile_id: int, profile_update: ProfileUpdate) -> ProfileRead:
    """Update a Profile while allowing partial updates."""

    profile = await _get_profile_or_error(session, profile_id)

    updated_data = {}

    if profile_update.avatar_url is not None:
        updated_data["avatar_url"] = profile_update.avatar_url

    if profile_update.bio is not None:
        updated_data["bio"] = profile_update.bio

    if profile_update.mood is not None:
        updated_data["mood"] = profile_update.mood

    if not updated_data:
        return _serialize_profile(profile)

    try:
        for key, value in updated_data.items():
            setattr(profile, key, value)
        
        await session.commit()
        await session.refresh(profile)

        return _serialize_profile(profile)
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating profile: {e}")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating profile: {e}")
    


async def _get_player_and_profile_or_error(session: AsyncSession, player_id: int) -> tuple[Player, Profile]:
    statement = (
        select(Player)
        .where(Player.id == player_id)
        .options(selectinload(Player.profile))
    )
    result = await session.execute(statement)

    player = result.scalar_one_or_none()

    if not player:
        raise PlayerNotFound(player_id)
    
    if player.profile:
        raise ProfileAlreadyExist(player_id)
    
    return (player, player.profile)

async def _get_profile_or_error(session: AsyncSession, profile_id: int) -> Profile:
    statement = (
        select(Profile)
        .where(Profile.id == profile_id)
        .options(joinedload(Profile.player))
    )

    result = await session.execute(statement)
    profile = result.scalar_one_or_none()

    if not profile:
        raise ProfileNotFound(profile_id)

    return profile

def _serialize_profile(profile: Profile) -> ProfileRead:
    return ProfileRead(
        id=profile.id,
        player_id=profile.player.id,
        avatar_url=profile.avatar_url,
        bio=profile.bio,
        mood=profile.mood
    )











