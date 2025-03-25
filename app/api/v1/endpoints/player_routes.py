from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.core.auth import get_current_user
from app.schemas.player_schema import PlayerCreate, PlayerRead
from app.crud.player_crud import crud_create_player, crud_read_all_players_with_users, crud_read_player_with_user

# router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])
router = APIRouter()

@router.post("/", response_model=PlayerCreate)
def create_player(  
    user_id: int, title: str = "Noobie", 
    level: int = 1, experience: int = 0, 
    session: Session = Depends(get_session)):
    return crud_create_player(session, user_id, title, level, experience)

@router.get("/read/id/{player_id}/", response_model=PlayerRead)
def read_player(player_id: int, session: Session = Depends(get_session)):
    try:
        return crud_read_player_with_user(session, player_id) 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/read/all", response_model=List[PlayerRead])
def read_all_players(session: Session = Depends(get_session)): 
    try:
        return crud_read_all_players_with_users(session) 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

