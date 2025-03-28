from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.subject_schema import SubjectCreate, SubjectRead, SubjectUpdate
from app.crud.subject_crud import crud_create_subject, crud_read_subject, crud_update_subject

router = APIRouter()

@router.post("/", response_model=SubjectRead)
def create_subject(player_id: int, new_subject: SubjectCreate, session: Session = Depends(get_session)):
    return crud_create_subject(session, player_id, new_subject)

@router.get("/{subject_id}", response_model=SubjectRead)
def read_subject(subject_id: int, session: Session = Depends(get_session)):
    return crud_read_subject(session, subject_id)

@router.patch("/{subject_id}", response_model=SubjectRead)
def update_subject(subject_id: int, updated_subject: SubjectUpdate, session: Session = Depends(get_session)):
    return crud_update_subject(session, subject_id, updated_subject)