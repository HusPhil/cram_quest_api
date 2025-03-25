from sqlmodel import Session, select
from typing import Optional, List
from sqlmodel import Session
from app.models.player_model import Player
from app.schemas.player_schema import PlayerRead
from app.models.user_model import User
from sqlalchemy.orm import joinedload

def crud_create_player(session: Session, id: int, title: str = "Noobie", level: int = 1, experience: int = 0) -> Player:
    user = session.get(User, id)
    if not user:
        raise ValueError(f"User with ID {id} not found.")

    db_player = Player(user_id=user.id, title=title, level=level, experience=experience)
    
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player

def crud_read_player_with_user(session: Session, player_id: int) -> PlayerRead:
    """Fetch a player along with their associated user data."""
    statement = (
        select(Player)
        .where(Player.id == player_id)
        .options(joinedload(Player.user))  # ✅ Automatically load the related User object
    )
    
    player = session.exec(statement).first()

    if not player:
        raise ValueError(f"Player with ID {player_id} not found.") # ✅ Return None if player does not exist
    
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
        select(User, Player)
        .join(Player, Player.id == User.id)
    )
    results = session.exec(statement).all() # Returns a list of tuples (User, Player)

    if not results:
        raise ValueError("No players found.")
    
    players_with_users = [
        PlayerRead(  # Create PlayerRead
            id=player.id,
            username=user.username,
            email=user.email,
            title=player.title,
            level=player.level,
            experience=player.experience
        )
        for user, player in results
    ]

    return players_with_users  # Return List[PlayerRead]
