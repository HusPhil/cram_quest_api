from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.schemas.quest_schema import QuestRead, QuestCreate, QuestUpdate
from app.crud.quest_crud import crud_create_quest, crud_read_quest, crud_update_quest, crud_read_all_quests, crud_delete_quest
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

# router = APIRouter()
router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])


@router.post("/", response_model=QuestRead)
async def create_quest(quest: QuestCreate, session: AsyncSession = Depends(get_session)):
    return await crud_create_quest(session, quest)

@router.get("/{quest_id}", response_model=QuestRead)
async def read_quest(quest_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_read_quest(session, quest_id)

@router.get("/", response_model=list[QuestRead])
async def read_all_quests(session: AsyncSession = Depends(get_session)):
    return await crud_read_all_quests(session)

@router.patch("/{quest_id}", response_model=QuestRead)
async def update_quest(quest_id: int, updated_quest: QuestUpdate, session: AsyncSession = Depends(get_session)):
    return await crud_update_quest(session, quest_id, updated_quest)

@router.delete("/{quest_id}", response_model=QuestRead)
async def delete_quest(quest_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_delete_quest(session, quest_id)