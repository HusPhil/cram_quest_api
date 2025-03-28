from sqlmodel import select
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Player, User

from app.schemas.player_schema import PlayerRead, PlayerCreate
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

class NoPlayersFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No players found")

async def crud_create_player(session: AsyncSession, user_id: int, player_create: PlayerCreate) -> PlayerRead:
    """Create a Player associated with a User, ensuring 1:1 relationship."""
    
    # check if a user does exists and if it already have an associated player
    user, player = await _get_user_and_player_or_error(session, user_id)

    # ✅ Create and persist the Player
    new_player = Player(
        user_id=user_id, 
        title=player_create.title, 
        level=player_create.level, 
        experience=player_create.experience
    )
    
    try:
        session.add(new_player)
        
        await session.commit()
        await session.refresh(new_player)
        
        return _serialize_player(new_player)
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise RuntimeError(f"Unexpected SQLAlchemyError while creating Player: {str(e)}")
    except Exception as e:
        await session.rollback()
        raise RuntimeError(f"Unexpected error while creating Player: {str(e)}")
    
async def crud_read_player_with_user(session: AsyncSession, player_id: int) -> PlayerRead:
    """Fetch a player along with their associated user data."""
    player = await _get_player_or_error(session, player_id)
    return _serialize_player(player)

async def crud_read_all_players_with_users(session: AsyncSession) -> List[PlayerRead]:
    """Fetch all players along with their associated user data."""
    statement = (
        select(Player)
        .options(joinedload(Player.user))  
    )
    players = await session.execute(statement) 
    players = players.scalars().all()  # Returns a list of tuples (User, Player)

    if not players:
        raise NoPlayersFound
    
    players_with_users = [_serialize_player(player) for player in players]

    return players_with_users  # Return List[PlayerRead]

def crud_read_all_player_subjects(session: AsyncSession, player_id: int) -> List[SubjectRead]:
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


async def _get_player_or_error(session: AsyncSession, player_id: int) -> Player:
    statement = (
        select(Player)
        .where(Player.id == player_id)
    )
    
    result = await session.execute(statement)

    player = result.scalar_one_or_none()

    if not player:
        raise PlayerNotFound(player_id)

    return player

async def _get_user_and_player_or_error(session: AsyncSession, user_id: int) -> tuple[User, Player]:
    statement = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.player))
    )
    result = await session.execute(statement)

    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFound
    
    if user.player:
        raise PlayerAlreadyExist(user.id)
    
    return (user, user.player)

def _serialize_player(player: Player) -> PlayerRead:
    return PlayerRead(
        id=player.id,
        user_id=player.user_id,
        title=player.title,
        level=player.level,
        experience=player.experience
    ) 



