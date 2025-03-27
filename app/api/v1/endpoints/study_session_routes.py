from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.study_session_schema import StudySessionRead, StudySessionCreate
from app.crud.study_session_crud import crud_create_study_session, crud_read_study_session, crud_end_study_session

router = APIRouter()


@router.post("/", response_model=StudySessionRead)
def create_subject(new_study_session: StudySessionCreate, session: Session = Depends(get_session)):
    return crud_create_study_session(session, new_study_session)

@router.get("/{study_session_id}", response_model=StudySessionRead)
def read_study_session(study_session_id: int, session: Session = Depends(get_session)):
    return crud_read_study_session(session, study_session_id)

@router.patch("/{study_session_id}", response_model=StudySessionRead)
def end_study_session(study_session_id: int, session: Session = Depends(get_session)):
    return crud_end_study_session(session, study_session_id)