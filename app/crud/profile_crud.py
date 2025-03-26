from sqlmodel import Session, select
from sqlmodel import Session
from fastapi import HTTPException
from app.models.player_model import Player
from app.schemas.profile_schema import ProfileRead
from app.models.profile_model import Profile
from app.crud.player_crud import PlayerNotFound
from sqlalchemy.orm import joinedload, selectinload

class ProfileNotFound(HTTPException):
    def __init__(self, profile_id: int):
        super().__init__(status_code=404, detail=f"Profile {profile_id} not found")

class ProfileAlreadyExist(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=400, detail=f"Profile already exists for player: {player_id}")

def crud_create_profile(session: Session, player_id: int, avatar_url: str, bio: str, mood: str):
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

    return profile

def crud_read_profile_with_user(session: Session, profile_id: int) -> ProfileRead:
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

def crud_read_all_profiles_with_users(session: Session) -> list[ProfileRead]:
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