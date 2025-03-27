from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models import Player, Subject
from app.crud.player_crud import PlayerNotFound
from app.schemas.subject_schema import SubjectRead, SubjectCreate, SubjectUpdate

class SubjectNotFound(HTTPException):
    def __init__(self, subject_id: int):
        super().__init__(status_code=404, detail=f"Subject {subject_id} not found")

class SubjectAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Subject already exists")

def crud_create_subject(session: Session, player_id: int, new_subject: SubjectCreate) -> SubjectRead:
    player = session.get(Player, player_id)

    if not player:
        raise PlayerNotFound(player_id)

    try:
        subject = Subject(
            player_id=player_id, 
            code_name=new_subject.code_name,
            description=new_subject.description, 
            difficulty=new_subject.difficulty
        )
        
        session.add(subject)
        session.commit()
        session.refresh(subject)

        return SubjectRead(
            id=subject.id, player_id=subject.player.id, 
            code_name=subject.code_name, description=subject.description, 
            difficulty=subject.difficulty
        )
    
    except SQLAlchemyError as e:
        session.rollback()
        if "difficulty_range" in str(e):  # ✅ Custom error message for difficulty constraint
            raise HTTPException(status_code=400, detail="Difficulty must be between 1 and 5.")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def crud_read_subject(session: Session, subject_id: int) -> SubjectRead:
    subject = session.get(Subject, subject_id)

    if not subject:
        raise SubjectNotFound(subject_id)
    
    return SubjectRead(
        id=subject.id, player_id=subject.player.id, 
        code_name=subject.code_name, description=subject.description, 
        difficulty=subject.difficulty
    )

def crud_update_subject(session: Session, subject_id: int, updated_subject: SubjectUpdate) -> SubjectRead:
    
    subject = session.get(Subject, subject_id)

    if not subject:
        raise SubjectNotFound(subject_id)
    
    updated_data = {}

    if updated_subject.code_name is not None:
        updated_data["code_name"] = updated_subject.code_name

    if updated_subject.description is not None:
        updated_data["description"] = updated_subject.description

    if updated_subject.difficulty is not None:
        updated_data["difficulty"] = updated_subject.difficulty

    if not updated_data:
        return SubjectRead(
            id=subject.id, player_id=subject.player.id, 
            code_name=subject.code_name, description=subject.description, 
            difficulty=subject.difficulty
        )

    try:
        for key, value in updated_data.items():
            setattr(subject, key, value)

        session.commit()
        session.refresh(subject)

        return SubjectRead(
            id=subject.id, player_id=subject.player.id, 
            code_name=subject.code_name, description=subject.description, 
            difficulty=subject.difficulty
        )
    
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    



