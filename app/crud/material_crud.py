from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlmodel import select

from app.models import Material
from app.schemas.material_schema import MaterialCreate, MaterialUpdate, MaterialRead


class MaterialNotFound(HTTPException):
    def __init__(self, material_id: int):
        super().__init__(status_code=404, detail=f"Material {material_id} not found")


async def crud_create_material(
    session: AsyncSession, subject_id: int, new_material: MaterialCreate
) -> MaterialRead:
    material = Material(
        subject_id=subject_id,
        title=new_material.title,
        type=new_material.type,
        link=new_material.link,
    )

    try:
        session.add(material)
        await session.commit()
        await session.refresh(material)
        return _serialize_material(material)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"SQLAlchemy error: {str(e)}")


async def crud_read_material(
    session: AsyncSession, material_id: int, subject_id: int
) -> MaterialRead:
    material = await _get_material_or_404(session, material_id)

    if material.subject_id != subject_id:
        raise HTTPException(status_code=404, detail="Material does not belong to this subject")

    return _serialize_material(material)


async def crud_read_all_subject_materials(
    session: AsyncSession, subject_id: int
) -> list[MaterialRead]:
    result = await session.scalars(select(Material).where(Material.subject_id == subject_id))
    materials = result.all()

    return [_serialize_material(m) for m in materials]


async def crud_update_material(
    session: AsyncSession, subject_id: int, material_id: int, updated: MaterialUpdate
) -> MaterialRead:
    material = await _get_material_or_404(session, material_id)

    if material.subject_id != subject_id:
        raise HTTPException(status_code=404, detail="Material does not belong to this subject")

    for field, value in updated.dict(exclude_unset=True).items():
        setattr(material, field, value)

    try:
        await session.commit()
        await session.refresh(material)
        return _serialize_material(material)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def crud_delete_material(session: AsyncSession, subject_id: int, material_id: int) -> MaterialRead:
    material = await _get_material_or_404(session, material_id)

    if material.subject_id != subject_id:
        raise HTTPException(status_code=403, detail="Material does not belong to the specified subject")

    try:
        await session.delete(material)
        await session.commit()
        return _serialize_material(material)
    
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def _get_material_or_404(session: AsyncSession, material_id: int) -> Material:
    result = await session.scalar(select(Material).where(Material.id == material_id))
    if not result:
        raise MaterialNotFound(material_id)
    return result


def _serialize_material(material: Material) -> MaterialRead:
    return MaterialRead(
        id=material.id,
        subject_id=material.subject_id,
        title=material.title,
        type=material.type,
        link=material.link,
    )