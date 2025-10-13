from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from stint_core.session_base import RaceSession

from app.database.db import get_db

from app.repositories.session import session_crud

router = APIRouter(prefix="/sessions", tags=["sessions"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_session(session: RaceSession, db: DbSession):
    try:
        race_session = session_crud.create(db, session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Session with id {session.session_id} already exists'
        ) from e
    return race_session
