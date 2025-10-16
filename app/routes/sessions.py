from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from stint_core.session_base import RaceSessionCreate

from app.database.db import get_db

from app.repositories import session_crud
from app.services.sheets_service import update_range

router = APIRouter(prefix="/sessions", tags=["sessions"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_session(session_create: RaceSessionCreate, db: DbSession, background_tasks: BackgroundTasks, sheet_id: str = None, sheet_range: str = None):
    
    try:
        race_session = session_crud.create(db, session_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Session with id {session_create.session_id} already exists'
        ) from e
    
    if sheet_id is not None:
        background_tasks.add_task(update_range, sheet_id, sheet_range, [race_session])
    return race_session