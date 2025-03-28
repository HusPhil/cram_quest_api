from sqlmodel import select, exists, and_, delete
from fastapi import HTTPException, status
from app.models import StudySession, Player, Subject, Quest
from app.models.quest_model import QuestStatus
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.study_session_model import SessionStatus
from app.crud.player_crud import PlayerNotFound
from app.crud.subject_crud import SubjectNotFound, SubjectNotBelongsToPlayer
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

class AccomplishedQuestLengthError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Accomplished quests cannot exceed the total selected quests")

class ValidationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to perform validation checks")



async def crud_create_study_session(session: AsyncSession, new_study_session: StudySessionCreate) -> StudySessionRead:

    await _validate_new_study_session(session, new_study_session)

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
        await session.commit()
        await session.refresh(study_session)

        return _serialize_study_session(study_session)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 

async def crud_read_study_session(session: AsyncSession, study_session_id: int) -> StudySessionRead:
    study_session = await _get_study_session_or_error(session, study_session_id)
    return _serialize_study_session(study_session)

async def crud_read_all_study_sessions(session: AsyncSession) -> list[StudySessionRead]:
    result = await session.scalars(select(StudySession))
    study_sessions = result.all()
    return [_serialize_study_session(study_session) for study_session in study_sessions]
    
async def crud_end_study_session(session: AsyncSession, study_session_id: int, session_end_data=StudySessionEnd) -> StudySessionRead:
    """Ends a study session, calculates XP, determines outcome, and removes accomplished quests."""
    
    if len(session_end_data.accomplished_quest_ids) > session_end_data.total_selected_quests:
        raise AccomplishedQuestLengthError

    # ✅ Fetch StudySession and validate existence in a **single query**
    study_session = await _get_study_session_or_error(session, study_session_id)
    
    # ✅ Fetch Accomplished Quests (Single Query)
    accomplished_quests = await _get_accomplished_quests(session, session_end_data, study_session.subject_id)

    print(accomplished_quests)
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
        await session.execute(delete(Quest).where(Quest.id.in_(session_end_data.accomplished_quest_ids)))


        # ✅ End the study session
        study_session.status = session_status
        study_session.end_time = datetime.now(timezone.utc)
        study_session.xp_earned = xp_earned

        await session.commit()  # Commit all changes in **one transaction**

        return _serialize_study_session(study_session)

    except Exception as e:
        session.rollback()  # Rollback changes on error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to end study session: {str(e)}")



async def _get_accomplished_quests(session: AsyncSession, session_end_data: StudySessionEnd, subject_id: int) -> list[Quest]:
    statement = (
        select(Quest)
        .where(
            Quest.id.in_(session_end_data.accomplished_quest_ids),
            Quest.subject_id == subject_id
        )
    )  
    result = await session.execute(statement)
    return result.scalars().all()  # ✅ Fetch multiple rows as a list

async def _get_study_session_or_error(session: AsyncSession, study_session_id: int) -> StudySession:
    """Helper function to retrieve a StudySession or raise 404 error."""
    study_session = await session.scalar(
        select(StudySession)
        .where(StudySession.id == study_session_id)
    )

    if study_session is None:
        raise StudySessionNotFound(study_session_id)
    
    if study_session.status == SessionStatus.COMPLETED:
        raise StudySessionAlreadyCompleted(study_session_id)
    
    return study_session

async def _validate_new_study_session(session: AsyncSession, new_study_session: StudySessionCreate):
    """
    Validates:
    1. Player exists
    2. Subject exists
    3. No active session exists
    4. Subject belongs to player
    """

    statement = select(
        exists().where(Player.id == new_study_session.player_id).label("player_exists"),
        exists().where(Subject.id == new_study_session.subject_id).label("subject_exists"),
        exists().where(
            and_(
                Subject.id == new_study_session.subject_id,
                Subject.player_id == new_study_session.player_id
            )
        ).label("subject_belongs_to_player"),
        exists().where(
            and_(
                StudySession.player_id == new_study_session.player_id,
                StudySession.status == SessionStatus.ACTIVE
            )
        ).label("has_active_session")
    )

    results = await session.execute(statement)
    validation_results = results.one_or_none()

    if not validation_results:
        raise ValidationError()
    
    player_exists, subject_exists, subject_belongs_to_player, has_active_session = validation_results
    
    if not player_exists:
        raise PlayerNotFound(new_study_session.player_id)

    if not subject_exists:
        raise SubjectNotFound(new_study_session.subject_id)

    if not subject_belongs_to_player:
        raise SubjectNotBelongsToPlayer(new_study_session.subject_id, new_study_session.player_id)

    if has_active_session:
        raise StudySessionStillActive(new_study_session.player_id)
    
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




