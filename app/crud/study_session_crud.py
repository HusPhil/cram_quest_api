from sqlmodel import Session, select, exists, and_
from fastapi import HTTPException, status
from app.models import StudySession, Player, Subject
from app.models.study_session_model import SessionStatus
from app.crud.player_crud import PlayerNotFound
from app.crud.subject_crud import SubjectNotFound
from app.schemas.study_session_schema import StudySessionRead, StudySessionCreate
from datetime import datetime, timezone, timedelta

class StudySessionStillActive(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=f"Player {player_id} already have an active study session")
    
class ValidationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to perform validation checks")

def crud_create_study_session(session: Session, new_study_session: StudySessionCreate) -> StudySessionRead:
    validation_results = utils_validate_inputs(session, new_study_session)

    if not validation_results:
        raise ValidationError
    
    player_exists, subject_exists, has_active_session = validation_results

    if not player_exists:
        raise PlayerNotFound(new_study_session.player_id)

    if not subject_exists:
        raise SubjectNotFound(new_study_session.subject_id)

    if has_active_session:
        raise StudySessionStillActive(new_study_session.player_id)

    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(minutes=new_study_session.duration_mins)

    study_session = StudySession(
        player_id=new_study_session.player_id,
        subject_id=new_study_session.subject_id,
        start_time=start_time,
        end_time=end_time,
    )

    session.add(study_session)
    session.commit()
    session.refresh(study_session)

    return StudySessionRead(
        id=study_session.id,
        player_id=study_session.player_id,
        subject_id=study_session.subject_id,
        start_time=study_session.start_time,
        end_time=study_session.end_time,
        xp_earned=study_session.xp_earned,
        status=study_session.status
    )

def crud_read_study_session(session: Session, study_session_id: int) -> StudySessionRead:
    study_session = session.get(StudySession, study_session_id)

    if study_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Study session {study_session_id} not found")
    
    return StudySessionRead(
        id=study_session.id,
        player_id=study_session.player_id,
        subject_id=study_session.subject_id,
        start_time=study_session.start_time,
        end_time=study_session.end_time,    
        xp_earned=study_session.xp_earned,
        status=study_session.status
    )

def crud_end_study_session(session: Session, study_session_id: int):
    study_session = session.get(StudySession, study_session_id)

    if study_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Study session {study_session_id} not found")

    study_session.status = SessionStatus.COMPLETED
    study_session.end_time = datetime.now(timezone.utc)

    session.add(study_session)
    session.commit()

    return StudySessionRead(
        id=study_session.id,
        player_id=study_session.player_id,
        subject_id=study_session.subject_id,
        start_time=study_session.start_time,
        end_time=study_session.end_time,
        xp_earned=study_session.xp_earned,
        status=study_session.status
    )


def utils_validate_inputs(session: Session, new_study_session: StudySessionCreate):
    validation_results = session.exec(
        select(
            exists().where(Player.id == new_study_session.player_id),
            exists().where(Subject.id == new_study_session.subject_id),
            select(StudySession).where(
                and_(
                    StudySession.player_id == new_study_session.player_id,
                    StudySession.status == SessionStatus.ACTIVE
                )
            ).exists()
        )
    ).first()

    return validation_results