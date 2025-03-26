from sqlmodel import Session, select
from typing import List
from fastapi import HTTPException
from sqlmodel import Session
from app.models.player_model import Player
from app.schemas.player_schema import PlayerRead
from app.models.user_model import User
from app.crud.user_crud import UserNotFound
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

class PlayerNotFound(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=404, detail=f"Player {player_id} not found")

class PlayerAlreadyExist(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"Player already exists for user: {user_id}")

def crud_create_player(session: Session, user_id: int, title: str = "Noobie", level: int = 1, experience: int = 0) -> Player:
    """Create a Player associated with a User, ensuring 1:1 relationship."""
    
    # 🔍 Ensure the User exists
    user = session.get(User, user_id)
    if not user:
        raise UserNotFound

    # 🚫 Prevent duplicate Player entries for the same User (Enforce 1:1)
    existing_player = session.exec(select(Player).where(Player.user_id == user_id)).first()
    if existing_player:
        raise PlayerAlreadyExist(user_id)

    # ✅ Create and persist the Player
    try:
        db_player = Player(user_id=user.id, title=title, level=level, experience=experience)
        session.add(db_player)
        session.commit()
        session.refresh(db_player)
        return db_player

    except IntegrityError as e:
        session.rollback()
        raise ValueError(f"Database error: {str(e)}")
    
def crud_read_player_with_user(session: Session, player_id: int) -> PlayerRead:
    """Fetch a player along with their associated user data."""
    statement = (
        select(Player)
        .where(Player.id == player_id)
        .options(joinedload(Player.user))  # ✅ Automatically load the related User object
    )
    
    player = session.exec(statement).first()

    if not player:
        raise PlayerNotFound(player_id)
    
    user = player.user

    if not user:
        raise ValueError(f"User for player with ID {player_id} not found.") # ✅ Return None if user does not exist
    
    return PlayerRead(
        id=player.id,
        username=user.username,
        email=user.email,
        title=player.title,
        level=player.level,
        experience=player.experience
    )

def crud_read_all_players_with_users(session: Session) -> List[PlayerRead]:
    """Fetch all players along with their associated user data."""
    statement = (
        select(Player)
        .options(joinedload(Player.user))  # ✅ Automatically load the related User object
    )
    players = session.exec(statement).all() # Returns a list of tuples (User, Player)

    if not players:
        raise ValueError("No players found.")
    
    players_with_users = [
        PlayerRead(  # Create PlayerRead
            id=player.id,
            username=player.user.username,
            email=player.user.email,
            title=player.title,
            level=player.level,
            experience=player.experience
        )
        for player in players
    ]

    return players_with_users  # Return List[PlayerRead]
