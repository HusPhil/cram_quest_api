from fastapi import HTTPException, status
from sqlmodel import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models import Player, Subject
from app.crud.player_crud import PlayerNotFound
from app.schemas.subject_schema import SubjectRead, SubjectCreate, SubjectUpdate

class SubjectNotFound(HTTPException):
    def __init__(self, subject_id: int):
        super().__init__(status_code=404, detail=f"Subject {subject_id} not found")

class SubjectAlreadyExists(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=400, detail=f"Player {player_id} already has this subject")

async def crud_create_subject(session: AsyncSession, player_id: int, new_subject: SubjectCreate) -> SubjectRead:
    
    await _validate_new_subject(session, player_id, new_subject)
    
    subject = Subject(
        player_id=player_id, 
        code_name=new_subject.code_name,
        description=new_subject.description, 
        difficulty=new_subject.difficulty
    )

    try:
        
        session.add(subject)
        await session.commit()
        await session.refresh(subject)

        return _serialize_subject(subject)
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"An SQLAlchemy error occurred: {str(e)}")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
async def crud_read_subject(session: AsyncSession, subject_id: int) -> SubjectRead:
    subject = await _get_subject_or_404(session, subject_id)
    return _serialize_subject(subject)

async def crud_update_subject(session: AsyncSession, subject_id: int, updated_subject: SubjectUpdate) -> SubjectRead:
    
    subject = await _get_subject_or_404(session, subject_id)
    
    updated_data = {}

    if updated_subject.code_name is not None:
        updated_data["code_name"] = updated_subject.code_name

    if updated_subject.description is not None:
        updated_data["description"] = updated_subject.description

    if updated_subject.difficulty is not None:
        updated_data["difficulty"] = updated_subject.difficulty

    if not updated_data:
        return _serialize_subject(subject)

    try:
        for key, value in updated_data.items():
            setattr(subject, key, value)

        await session.commit()
        await session.refresh(subject)

        return _serialize_subject(subject)
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
async def crud_delete_subject(session: AsyncSession, subject_id: int) -> SubjectRead:
    subject = await _get_subject_or_404(session, subject_id)

    try:
        await session.delete(subject)
        await session.commit()

        return _serialize_subject(subject)
    
    except SQLAlchemyError as e:
        await session.rollback()

async def _validate_new_subject(session: AsyncSession, player_id: int, new_subject: SubjectCreate) -> None:
    statement = select(
        exists().where(Player.id == player_id),  # ✅ Check if Player exists
        exists().where(
            (Subject.player_id == player_id) & (Subject.code_name == new_subject.code_name)  # ✅ Check if Subject exists
        )
    )

    result = await session.execute(statement)
    player_exists, subject_exists = result.first()
    
    if not player_exists:
        raise PlayerNotFound(player_id)
    
    if subject_exists:
        raise SubjectAlreadyExists(player_id)

async def _get_subject_or_404(session: AsyncSession, subject_id: int) -> Subject:
    statement = select(Subject).where(Subject.id == subject_id)

    subject = await session.scalar(statement)

    if not subject:
        raise SubjectNotFound(subject_id)

    return subject

def _serialize_subject(subject: Subject) -> SubjectRead:
    return SubjectRead(
        id=subject.id, player_id=subject.player_id, 
        code_name=subject.code_name, description=subject.description, 
        difficulty=subject.difficulty
    )