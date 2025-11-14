from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.session_schemas import RaceSessionCreate, RaceSessionRead

from app.database.db import get_db
from app.models import RaceSession
from app.repositories import session_crud

router = APIRouter(prefix="/sessions", tags=["sessions"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[RaceSessionRead])
def list_sessions(
    db: DbSession,
    session_date: Optional[str] = None,
    track: Optional[str] = None,
    car_class: Optional[str] = None,
    car: Optional[str] = None,
):
    sessions = session_crud.get_many(
        db,
        session_date=session_date,
        track=track,
        car_class=car_class,
        car=car,
    )
    return sessions


@router.get("/{session_id}", response_model=RaceSessionRead)
def get_session(session_id: int, db: DbSession):
    session = session_crud.get_one(db, RaceSession.id == session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )

    return session


@router.post("", response_model=RaceSessionRead)
def create_session(session_create: RaceSessionCreate, db: DbSession):

    try:
        race_session = session_crud.create(db, session_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Session with id {session_create.id} already exists",
        ) from e

    return race_session
