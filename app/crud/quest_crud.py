from sqlmodel import select, and_, exists
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Quest, Subject
from app.schemas.quest_schema import QuestRead, QuestCreate, QuestUpdate, QuestStatus
from app.crud.subject_crud import SubjectNotFound
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


async def crud_create_quest(session: AsyncSession, new_quest: QuestCreate) -> QuestRead:
    """ Create a new quest with validation """
    # Check for existing quest
    
    await _validate_new_quest(session, new_quest)
    
    # Create new quest
    quest = Quest(
        subject_id=new_quest.subject_id,
        description=new_quest.description,
        difficulty=new_quest.difficulty
    )

    try:
        session.add(quest)
        await session.commit()
        await session.refresh(quest)
        
        return _serialize_quest(quest)
        
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create quest: {str(e)}"
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create quest: {str(e)}"
        )

async def crud_update_quest(session: AsyncSession, quest_id: int, updated_quest: QuestUpdate) -> QuestRead:
    
    quest_to_update = await _get_quest_or_error(session, quest_id)

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

        await session.commit()
        await session.refresh(quest_to_update)

        return _serialize_quest(quest_to_update)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update quest: {str(e)}"
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update quest: {str(e)}"
        )
    
async def crud_read_quest(session: AsyncSession, quest_id: int) -> QuestRead:
    quest = await _get_quest_or_error(session, quest_id)
    return _serialize_quest(quest)

async def crud_read_all_quests(session: AsyncSession) -> list[QuestRead]:
    result = await session.scalars(
        select(Quest)
    )

    quests = result.all()

    return [_serialize_quest(quest) for quest in quests]

async def crud_delete_quest(session: AsyncSession, quest_id: int) -> None:
    quest = await _get_quest_or_error(session, quest_id)

    try:
        await session.delete(quest)
        await session.commit()
        return _serialize_quest(quest)
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete quest: {str(e)}"
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete quest: {str(e)}"
        )


async def _validate_new_quest(session: AsyncSession, new_quest: QuestCreate) -> None:
    result = await session.execute(
        select(
            exists()
            .where(and_(
                Quest.subject_id == new_quest.subject_id,
                Quest.description == new_quest.description
            )).label("quest_exists"),
            exists()
            .where(Subject.id == new_quest.subject_id).label("subject_exists")
        )
    )
    

    quest_exists, subject_exists = result.one_or_none() 



    if quest_exists:
        raise QuestAlreadyExists(new_quest.subject_id)

    if not subject_exists:
        raise SubjectNotFound(new_quest.subject_id)

async def _get_quest_or_error(session: AsyncSession, quest_id: int) -> Quest:
    quest = await session.scalar(
        select(Quest)
        .where(Quest.id == quest_id)
    )

    if not quest:
        raise QuestNotFound(quest_id)

    return quest

def _serialize_quest(quest: Quest) -> QuestRead:
    return QuestRead(
        id=quest.id,
        subject_id=quest.subject_id,
        description=quest.description,
        difficulty=quest.difficulty,
        status=quest.status,
        created_at=quest.created_at
    )
