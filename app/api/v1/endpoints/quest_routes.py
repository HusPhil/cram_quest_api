from fastapi import APIRouter, Depends
from app.schemas.quest_schema import QuestRead, QuestCreate, QuestUpdate
from app.crud.quest_crud import crud_create_quest, crud_read_quest, crud_update_quest
from app.core.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.post("/", response_model=QuestRead)
def create_quest(quest: QuestCreate, session: Session = Depends(get_session)):
    return crud_create_quest(session, quest)

@router.get("/{quest_id}", response_model=QuestRead)
def read_quest(quest_id: int, session: Session = Depends(get_session)):
    return crud_read_quest(session, quest_id)

@router.patch("/{quest_id}", response_model=QuestRead)
def update_quest(quest_id: int, updated_quest: QuestUpdate, session: Session = Depends(get_session)):
    return crud_update_quest(session, quest_id, updated_quest)