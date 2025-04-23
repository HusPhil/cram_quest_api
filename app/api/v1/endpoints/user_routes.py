from fastapi import APIRouter, Depends
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.crud.user_crud import crud_create_user, crud_read_user_by_id, crud_read_all_users, crud_update_user, crud_delete_user, crud_read_user_player
from app.core.auth import get_current_user

from app.schemas.player_schema import PlayerRead


router = APIRouter(dependencies=[Depends(get_session)])
# router = APIRouter()
 
@router.post("/", response_model=UserRead)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    return await crud_create_user(session, user_create)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    return await crud_update_user(session, user_id, user_update)

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_read_user_by_id(session, user_id)

@router.get("/{user_id}/player", response_model=PlayerRead)
async def read_user_player(user_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_read_user_player(session, user_id)

@router.get("/", response_model=list[UserRead])
async def read_all_users(session: AsyncSession = Depends(get_session)):
    return await crud_read_all_users(session)

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_delete_user(session, user_id)

