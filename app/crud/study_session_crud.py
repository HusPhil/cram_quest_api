from sqlmodel import Session, select, exists, and_, delete
from fastapi import HTTPException, status
from app.models import StudySession, Player, Subject, Quest
from app.models.study_session_model import SessionStatus
from app.crud.player_crud import PlayerNotFound
from app.crud.subject_crud import SubjectNotFound
from app.schemas.study_session_schema import StudySessionRead, StudySessionCreate, StudySessionEnd
from app.services.game_service import GameService
from datetime import datetime, timezone, timedelta

class StudySessionStillActive(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=f"Player {player_id} already have an active study session")

class StudySessionAlreadyCompleted(HTTPException):
    def __init__(self, study_session_id: int):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=f"Study session {study_session_id} already completed")

class StudySessionNotFound(HTTPException):
    def __init__(self, study_session_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Study session {study_session_id} not found")
    
class ValidationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to perform validation checks")

def crud_create_study_session(session: Session, new_study_session: StudySessionCreate) -> StudySessionRead:

    _validate_inputs(session, new_study_session)

    start_time = datetime.now().replace(tzinfo=timezone.utc)
    end_time = start_time + timedelta(minutes=new_study_session.duration_mins)

    study_session = StudySession(
        player_id=new_study_session.player_id,
        subject_id=new_study_session.subject_id,
        start_time=start_time,
        end_time=end_time,
    )

    try:
        session.add(study_session)
        session.commit()
        session.refresh(study_session)

        return _serialize_study_session(study_session)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 

def crud_read_study_session(session: Session, study_session_id: int) -> StudySessionRead:
    study_session = session.get(StudySession, study_session_id)

    if study_session is None:
        raise StudySessionNotFound(study_session_id)
    
    return _serialize_study_session(study_session)

def crud_read_all_study_sessions(session: Session) -> list[StudySessionRead]:
    study_sessions = session.exec(select(StudySession)).all()

    return [_serialize_study_session(study_session) for study_session in study_sessions]
    
def crud_end_study_session(session: Session, study_session_id: int, session_end_data=StudySessionEnd) -> StudySessionRead:
    """Ends a study session, calculates XP, determines outcome, and removes accomplished quests."""
    
    if len(session_end_data.accomplished_quest_ids) > session_end_data.total_selected_quests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Accomplished quests cannot exceed total selected quests"
        )

    # ✅ Fetch StudySession and validate existence in a **single query**
    study_session = _get_study_session_or_404(session, study_session_id)
    
    
    # ✅ Fetch Accomplished Quests (Single Query)
    accomplished_quests = session.exec(
        select(Quest).where(Quest.id.in_(session_end_data.accomplished_quest_ids))
    ).all()

    # ✅ Ensure All Accomplished Quest IDs Exist
    found_quest_ids = {quest.id for quest in accomplished_quests}
    requested_quest_ids = set(session_end_data.accomplished_quest_ids)

    if found_quest_ids != requested_quest_ids:
        missing_quests = requested_quest_ids - found_quest_ids
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Quests not found: {missing_quests}")
    
    try:

        # ✅ Determine Outcome (Win, Defeat, or Canceled)
        completion_rate = len(accomplished_quests) / session_end_data.total_selected_quests

        if completion_rate == 1.0:
            session_status = SessionStatus.COMPLETED  # 🏆 Win (All tasks done)
        else:
            session_status = SessionStatus.DEFEAT  # ⚔️ Partial completion = Defeat

        # ✅ Calculate XP based on outcome
        xp_earned = GameService.calculate_xp(
            study_session,
            accomplished_quests,
            session_end_data.total_selected_quests,
            session_status
        )

        # ✅ Bulk Delete Accomplished Quests (Faster than looping)
        session.exec(delete(Quest).where(Quest.id.in_(session_end_data.accomplished_quest_ids)))

        # ✅ End the study session
        study_session.status = session_status
        study_session.end_time = datetime.now(timezone.utc)
        study_session.xp_earned = xp_earned

        session.commit()  # Commit all changes in **one transaction**

        return _serialize_study_session(study_session)

    except Exception as e:
        session.rollback()  # Rollback changes on error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to end study session: {str(e)}")


def _get_study_session_or_404(session: Session, study_session_id: int) -> StudySession:
    """Helper function to retrieve a StudySession or raise 404 error."""
    study_session = session.get(StudySession, study_session_id)

    if study_session is None:
        raise StudySessionNotFound(study_session_id)
    
    if study_session.status == SessionStatus.COMPLETED:
        raise StudySessionAlreadyCompleted(study_session_id)
    
    return study_session

def _serialize_study_session(study_session: StudySession) -> StudySessionRead:
    """Helper function to convert a StudySession into a StudySessionRead schema."""
    return StudySessionRead(
        id=study_session.id,
        player_id=study_session.player_id,
        subject_id=study_session.subject_id,
        start_time=study_session.start_time,
        end_time=study_session.end_time,
        xp_earned=study_session.xp_earned,
        status=study_session.status
    )

def _validate_inputs(session: Session, new_study_session: StudySessionCreate):
    """
    Validates:
    1. Player exists
    2. Subject exists
    3. No active session exists
    4. Subject belongs to player
    """
    validation_results = session.exec(
        select(
            exists().where(Player.id == new_study_session.player_id),
            exists().where(Subject.id == new_study_session.subject_id),
            exists().where(
                and_(
                    Subject.id == new_study_session.subject_id,
                    Subject.player_id == new_study_session.player_id
                )
            ),
            select(StudySession)
            .where(
                and_(
                    StudySession.player_id == new_study_session.player_id,
                    StudySession.status == SessionStatus.ACTIVE
                )
            )
            .exists()
        )
    ).first()

    if not validation_results:
        raise ValidationError()

    player_exists, subject_exists, subject_belongs_to_player, has_active_session = validation_results

    if not player_exists:
        raise PlayerNotFound(new_study_session.player_id)

    if not subject_exists:
        raise SubjectNotFound(new_study_session.subject_id)

    if not subject_belongs_to_player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Subject {new_study_session.subject_id} does not belong to player {new_study_session.player_id}"
        )

    if has_active_session:
        raise StudySessionStillActive(new_study_session.player_id)
    


