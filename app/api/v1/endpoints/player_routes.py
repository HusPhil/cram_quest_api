from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.core.auth import get_current_user, get_current_admin
from app.schemas.player_schema import PlayerCreate, PlayerRead
from app.schemas.subject_schema import SubjectRead
from app.crud.player_crud import crud_create_player, crud_read_all_players_with_users, crud_read_player_with_user, crud_read_all_player_subjects
from app.models import User

router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])
# router = APIRouter()

@router.post("/{user_id}", response_model=PlayerRead)
async def create_player(user_id: int, player_create: PlayerCreate, session: Session = Depends(get_session)):
    return await crud_create_player(session, user_id, player_create)

@router.get("/{player_id}/", response_model=PlayerRead)
async def read_player(player_id: int, session: Session = Depends(get_session)):
    return await crud_read_player_with_user(session, player_id)
    
@router.get("", response_model=List[PlayerRead])
async def read_all_players(session: Session = Depends(get_session), admin_user: User = Depends(get_current_admin)):
    if not admin_user.is_admin  :
        raise HTTPException(status_code=403, detail="Not enough permissions") 
    return await crud_read_all_players_with_users(session)
    
@router.get("/{player_id}/subjects", response_model=List[SubjectRead])
async def read_all_player_subjects(player_id: int, session: Session = Depends(get_session)):
    return await crud_read_all_player_subjects(session, player_id)



