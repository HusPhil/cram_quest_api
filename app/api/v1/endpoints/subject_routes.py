from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_user

from app.core.database import get_session
from app.schemas.subject_schema import SubjectCreate, SubjectRead, SubjectUpdate
from app.schemas.quest_schema import QuestRead
from app.crud.subject_crud import crud_create_subject, crud_read_subject, crud_update_subject, crud_delete_subject, crud_read_subject_all_quests

from app.schemas.material_schema import MaterialCreate, MaterialUpdate, MaterialRead
from app.crud.material_crud import (
    crud_create_material,
    crud_read_material,
    crud_read_all_subject_materials,
    crud_update_material,
    crud_delete_material
)


# router = APIRouter()
router = APIRouter(dependencies=[Depends(get_session), Depends(get_current_user)])

@router.post("/", response_model=SubjectRead)
async def create_subject(player_id: int, subject_create: SubjectCreate, session: AsyncSession = Depends(get_session)):
    return await crud_create_subject(session, player_id, subject_create)

@router.get("/{subject_id}", response_model=SubjectRead)
async def read_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_read_subject(session, subject_id)

@router.get("/{subject_id}/quests", response_model=list[QuestRead])
async def read_subject_quests(subject_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_read_subject_all_quests(session, subject_id)

@router.patch("/{subject_id}", response_model=SubjectRead)
async def update_subject(subject_id: int, updated_subject: SubjectUpdate, session: AsyncSession = Depends(get_session)):
    return await crud_update_subject(session, subject_id, updated_subject)

@router.delete("/{subject_id}", response_model=SubjectRead)
async def delete_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_delete_subject(session, subject_id)






# CREATE material
@router.post("/{subject_id}/materials", response_model=MaterialRead)
async def create_material(
    subject_id: int,
    material_create: MaterialCreate,
    session: AsyncSession = Depends(get_session)
):
    return await crud_create_material(session, subject_id, material_create)

# READ all materials under subject
@router.get("/{subject_id}/materials", response_model=list[MaterialRead])
async def read_all_materials(
    subject_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await crud_read_all_subject_materials(session, subject_id)

# READ one material
@router.get("/{subject_id}/materials/{material_id}", response_model=MaterialRead)
async def read_material(
    subject_id: int,
    material_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await crud_read_material(session, material_id, subject_id)

# UPDATE material
@router.patch("/{subject_id}/materials/{material_id}", response_model=MaterialRead)
async def update_material(
    subject_id: int,
    material_id: int,
    material_update: MaterialUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await crud_update_material(session, subject_id, material_id, material_update)


@router.delete("/{subject_id}/materials/{material_id}", response_model=MaterialRead)
async def delete_material(
    subject_id: int,
    material_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await crud_delete_material(session, subject_id, material_id)