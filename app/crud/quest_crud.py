from sqlmodel import Session, select, and_
from fastapi import HTTPException, status
from app.models import Quest
from app.schemas.quest_schema import QuestRead, QuestCreate, QuestUpdate, QuestStatus
from app.crud.player_crud import PlayerNotFound
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

class QuestNotFound(HTTPException):
    def __init__(self, quest_id: int):
        super().__init__(status_code=404, detail=f"Quest {quest_id} not found")

class QuestAlreadyExists(HTTPException):
    def __init__(self, subject_id: int):
        super().__init__(status_code=400, detail=f"Quest already exists for subject {subject_id}")

class QuestAlreadyCompleted(HTTPException):
    def __init__(self, quest_id: int):
        super().__init__(status_code=409, detail=f"Quest {quest_id} already completed")


def crud_create_quest(session: Session, new_quest: QuestCreate) -> QuestRead:
    """ Create a new quest with validation """
    # Check for existing quest
    if _check_quest_exists_in_subject(session, new_quest.description, new_quest.subject_id):
        raise QuestAlreadyExists
    
    # Create new quest
    quest = Quest(
        subject_id=new_quest.subject_id,
        description=new_quest.description,
        difficulty=new_quest.difficulty
    )

    try:
        session.add(quest)
        session.commit()
        session.refresh(quest)
        
        return QuestRead(
            id=quest.id,
            subject_id=quest.subject_id,
            description=quest.description,
            difficulty=quest.difficulty,
            status=quest.status,
            created_at=quest.created_at
        )
        
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create quest: {str(e)}"
        )

def crud_update_quest(session: Session, quest_id: int, updated_quest: QuestUpdate) -> QuestRead:
    
    quest_to_update = session.exec(select(Quest).where(Quest.id == quest_id)).first()

    if not quest_to_update:
        raise QuestNotFound(quest_id)
    
    updated_data = {}

    if updated_quest.description:
        updated_data["description"] = updated_quest.description

    if updated_quest.difficulty:
        updated_data["difficulty"] = updated_quest.difficulty

    if updated_quest.status:
        updated_data["status"] = updated_quest.status

    if not updated_data:
        return QuestRead(
            id=quest_to_update.id,
            subject_id=quest_to_update.subject_id,
            description=quest_to_update.description,
            difficulty=quest_to_update.difficulty,
            status=quest_to_update.status,
            created_at=quest_to_update.created_at
        )

    try:    
        for key, value in updated_data.items():
            setattr(quest_to_update, key, value)

        session.commit()
        session.refresh(quest_to_update)

        return QuestRead(
            id=quest_to_update.id,
            subject_id=quest_to_update.subject_id,
            description=quest_to_update.description,
            difficulty=quest_to_update.difficulty,
            status=quest_to_update.status,
            created_at=quest_to_update.created_at
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update quest: {str(e)}"
        )
    
def crud_read_quest(session: Session, quest_id: int) -> QuestRead:
    quest = session.get(Quest, quest_id)

    if not quest:
        raise QuestNotFound(quest_id)

    return QuestRead(
        id=quest.id,
        subject_id=quest.subject_id,
        description=quest.description,
        difficulty=quest.difficulty,
        status=quest.status,
        created_at=quest.created_at
    )


def _check_quest_exists_in_subject(session: Session, description: str, subject_id: int) -> Optional[Quest]:
    """Check if a quest with same description and subject exists"""
    return session.exec(
        select(Quest).where(
            and_(
                Quest.description == description,
                Quest.subject_id == subject_id
            )
        )
    ).first()

