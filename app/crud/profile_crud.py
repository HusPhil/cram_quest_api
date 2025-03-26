from sqlmodel import Session, select
from sqlmodel import Session
from app.models.player_model import Player
from app.models.profile_model import Profile
from app.crud.player_crud import PlayerNotFound

# class ProfileCreate(Profile):
#     avatar_url: str = "default.png"
#     bio: Optional[str] = ""
#     mood: Optional[Mood] = Mood.NEUTRAL

def crud_create_profile(session: Session, player_id: int, avatar_url: str, bio: str, mood: str):
    player = session.get(Player, player_id)

    if not player:
        raise PlayerNotFound(player_id)
    
    profile = Profile(player_id=player_id, avatar_url=avatar_url, bio=bio, mood=mood)
    session.add(profile)
    session.commit()
    session.refresh(profile)

    return profile