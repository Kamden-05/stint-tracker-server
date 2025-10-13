from fastapi import APIRouter, Depends
from stint_core.stint_base import StintCreate, StintUpdate 
from app.database.db import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.repositories import stint_crud, session_crud
from app.models.session import Session as RaceSession


router = APIRouter(prefix='/stints', tags=['stints'])

DbSession = Annotated[Session, Depends(get_db)]

@router.post("/{session_id}")
def create_stint(session_id: int, stint_create: StintCreate, db: DbSession):
    session = session_crud.get_one(db, RaceSession.id == session_id)
    return
    

@router.put("/{session_id}/update/{stint_id}")
def update_stint(session_id: int, stint: StintUpdate):
    return stint