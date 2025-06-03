from typing import Optional, TYPE_CHECKING
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column, String
from sqlalchemy import ForeignKey
from app.schemas.subject_schema import SubjectMaterialType


if TYPE_CHECKING:
    from app.models import Subject

class Material(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    title: str = Field(sa_column=Column(String, nullable=False))
    type: SubjectMaterialType = Field(
        sa_column=Column(String, nullable=False)
    )
    link: str = Field(sa_column=Column(String, nullable=False))

    subject_id: int = Field(
        sa_column=Column(ForeignKey("subject.id", ondelete="CASCADE"), nullable=False, index=True)
    )

    subject: Optional["Subject"] = Relationship(back_populates="materials")


