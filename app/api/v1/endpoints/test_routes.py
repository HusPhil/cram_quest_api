from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from sqlalchemy import text

router = APIRouter()

@router.get("/debug/foreign_keys/")
def check_foreign_keys(session: Session = Depends(get_session)):
    result = session.exec(text("PRAGMA foreign_keys;")).fetchone()
    return {"foreign_keys_enabled": bool(result[0])}