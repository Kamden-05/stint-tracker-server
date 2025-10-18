from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from stint_core.session_base import RaceSessionCreate

from app.database.db import get_db

from app.repositories import session_crud

router = APIRouter(prefix="/sessions", tags=["sessions"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_session(session_create: RaceSessionCreate, db: DbSession):
    
    try:
        race_session = session_crud.create(db, session_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Session with id {session_create.session_id} already exists'
        ) from e
    return race_session