from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.schemas.player_schema import PlayerCreate, PlayerRead
from app.crud.player_crud import create_player, get_player_with_user, get_all_players_with_users

router = APIRouter()

@router.post("/", response_model=PlayerCreate)
def create_player(
    user_id: int, title: str = "Noobie", 
    level: int = 1, experience: int = 0, 
    session: Session = Depends(get_session)):
    return create_player(session, user_id, title, level, experience)

@router.get("/get_player/id/{player_id}/", response_model=PlayerRead)
def read_player(player_id: int, session: Session = Depends(get_session)):
    try:
        return get_player_with_user(session, player_id) 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/get_player/all", response_model=List[PlayerRead])
def read_all_players(session: Session = Depends(get_session)): 
    try:
        return get_all_players_with_users(session) 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

