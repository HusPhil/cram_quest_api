from sqlmodel import Session, select
from sqlmodel import Session
from fastapi import HTTPException
from app.models.player_model import Player
from app.schemas.profile_schema import ProfileRead, ProfileUpdate
from app.models.profile_model import Profile
from app.crud.player_crud import PlayerNotFound
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError

class ProfileNotFound(HTTPException):
    def __init__(self, profile_id: int):
        super().__init__(status_code=404, detail=f"Profile {profile_id} not found")

class ProfileAlreadyExist(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=400, detail=f"Profile already exists for player: {player_id}")

def crud_create_profile(session: Session, player_id: int, avatar_url: str, bio: str, mood: str) -> ProfileRead:
    statement = (
        select(Player)
        .where(Player.id == player_id)
        .options(selectinload(Player.profile))
    )

    player = session.exec(statement).first()

    if not player:
        raise PlayerNotFound(player_id)
    
    if player.profile:
        raise ProfileAlreadyExist(player_id)

    profile = Profile(player_id=player_id, avatar_url=avatar_url, bio=bio, mood=mood)
    session.add(profile)    
    session.commit()
    session.refresh(profile)

    return ProfileRead(
        id=profile.id,
        player_id=profile.player.id,
        avatar_url=profile.avatar_url,
        bio=profile.bio,
        mood=profile.mood
    )

def crud_read_profile(session: Session, profile_id: int) -> ProfileRead:
    statement = (
        select(Profile)
        .where(Profile.id == profile_id)
        .options(joinedload(Profile.player))
    )

    profile = session.exec(statement).first()

    if not profile:
        raise ProfileNotFound(profile_id)

    return ProfileRead(
        id=profile.id,
        player_id=profile.player.id,
        avatar_url=profile.avatar_url,
        bio=profile.bio,
        mood=profile.mood
    )

def crud_read_all_profiles(session: Session) -> list[ProfileRead]:
    statement = (
        select(Profile)
        .options(joinedload(Profile.player))
    )

    profiles = session.exec(statement).all()

    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found")

    profiles_with_users = [
        ProfileRead(
            id=profile.id,
            player_id=profile.player.id,
            avatar_url=profile.avatar_url,
            bio=profile.bio,
            mood=profile.mood
        )
        for profile in profiles
    ]

    return profiles_with_users

def crud_update_profile(session: Session, profile_id: int, profile_update: ProfileUpdate) -> ProfileRead:
    """Update a Profile while allowing partial updates."""

    profile = session.get(Profile, profile_id)

    if not profile:
        raise ProfileNotFound(profile_id)

    updated_data = {}

    if profile_update.avatar_url is not None:
        updated_data["avatar_url"] = profile_update.avatar_url

    if profile_update.bio is not None:
        updated_data["bio"] = profile_update.bio

    if profile_update.mood is not None:
        updated_data["mood"] = profile_update.mood

    if not updated_data:
        raise ProfileRead(
            id=profile.id,
            player_id=profile.player.id,
            avatar_url=profile.avatar_url,
            bio=profile.bio,
            mood=profile.mood
        )

    try:
        for key, value in updated_data.items():
            setattr(profile, key, value)
        session.commit()
        session.refresh(profile)

        return ProfileRead(
            id=profile.id,
            player_id=profile.player.id,
            avatar_url=profile.avatar_url,
            bio=profile.bio,
            mood=profile.mood
        )
    
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating profile: {e}")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating profile: {e}")