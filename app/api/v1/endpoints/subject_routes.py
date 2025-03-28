from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_user

from app.core.database import get_session
from app.schemas.subject_schema import SubjectCreate, SubjectRead, SubjectUpdate
from app.crud.subject_crud import crud_create_subject, crud_read_subject, crud_update_subject, crud_delete_subject

# router = APIRouter()
router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])

@router.post("/", response_model=SubjectRead)
async def create_subject(player_id: int, subject_create: SubjectCreate, session: AsyncSession = Depends(get_session)):
    return await crud_create_subject(session, player_id, subject_create)

@router.get("/{subject_id}", response_model=SubjectRead)
async def read_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_read_subject(session, subject_id)

@router.patch("/{subject_id}", response_model=SubjectRead)
async def update_subject(subject_id: int, updated_subject: SubjectUpdate, session: AsyncSession = Depends(get_session)):
    return await crud_update_subject(session, subject_id, updated_subject)

@router.delete("/{subject_id}", response_model=SubjectRead)
async def delete_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_delete_subject(session, subject_id)