from sqlmodel import Session, select
from typing import List
from fastapi import HTTPException
from sqlmodel import Session

from app.models import Player, User

from app.schemas.player_schema import PlayerRead
from app.schemas.subject_schema import SubjectRead

from app.crud.user_crud import UserNotFound

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class PlayerNotFound(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=404, detail=f"Player {player_id} not found")

class PlayerAlreadyExist(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"Player already exists for user: {user_id}")

def crud_create_player(session: Session, user_id: int, title: str = "Noobie", level: int = 1, experience: int = 0) -> Player:
    """Create a Player associated with a User, ensuring 1:1 relationship."""
    
    # ✅ Perform a single query to check both User existence & Player existence
    statement = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.player))
    )

    user = session.exec(statement).first()

    if not user:
        raise UserNotFound(f"User with ID {user_id} not found.")

    if user.player:  # ✅ Check if Player already exists
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
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating Player: {str(e)}")
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Unexpected error while creating Player: {str(e)}")
    
def crud_read_player_with_user(session: Session, player_id: int) -> PlayerRead:
    """Fetch a player along with their associated user data."""
    statement = (
        select(Player)
        .where(Player.id == player_id)
        .options(joinedload(Player.user))
    )
    
    player = session.exec(statement).first()

    if not player:
        raise PlayerNotFound(player_id)
    
    user = player.user

    if not user:
        raise ValueError(f"User for player with ID {player_id} not found.") 
    
    return PlayerRead(
        id=player.id,
        user_id=user.id,
        title=player.title,
        level=player.level,
        experience=player.experience
    )

def crud_read_all_players_with_users(session: Session) -> List[PlayerRead]:
    """Fetch all players along with their associated user data."""
    statement = (
        select(Player)
        .options(joinedload(Player.user))  
    )
    players = session.exec(statement).all() # Returns a list of tuples (User, Player)

    if not players:
        raise ValueError("No players found.")
    
    players_with_users = [
        PlayerRead(
            id=player.id,
            user_id=player.user.id,
            title=player.title,
            level=player.level,
            experience=player.experience
        )
        for player in players
    ]

    return players_with_users  # Return List[PlayerRead]

def crud_read_all_player_subjects(session: Session, player_id: int) -> List[SubjectRead]:
    statement = (
        select(Player)
        .where(Player.id == player_id)
        .options(selectinload(Player.subjects))
    )

    player = session.exec(statement).first()

    if not player:
        raise PlayerNotFound(player_id)

    return [
        SubjectRead(
            id=subject.id,
            player_id=subject.player.id,
            code_name=subject.code_name,
            description=subject.description,
            difficulty=subject.difficulty
        )
        for subject in player.subjects
    ]   