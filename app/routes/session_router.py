from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.session_schemas import (
    RaceSessionCreate,
    RaceSessionRead,
    SessionCarRead,
)

from app.schemas.report_schemas import RaceReport

from app.database.db import get_db
from app.models import RaceSession
from app.repositories import session_crud, session_car_crud
from app.services import generate_race_summary
from app.dependencies import SessionCarDep, DbSessionDep

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", response_model=list[RaceSessionRead])
def list_sessions(
    db: DbSessionDep,
    session_date: Optional[str] = None,
    track: Optional[str] = None,
):
    sessions = session_crud.get_many(
        db,
        session_date=session_date,
        track=track,
    )

    logger.info(
        "Listing sessions with filters: date=%s, track=%s",
        session_date,
        track,
    )

    return sessions


@router.get("/{session_id}", response_model=RaceSessionRead)
def get_session(session_id: int, db: DbSessionDep):
    session = session_crud.get_one(db, RaceSession.id == session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )

    return session


@router.post("", response_model=SessionCarRead)
def create_session(session_create: RaceSessionCreate, db: DbSessionDep):
    session_data = session_create.model_dump(
        exclude={"car_id", "car_name", "car_class"}
    )

    try:
        race_session = session_crud.create(db, session_data)
        logger.info(
            "Creating session for id=%s date=%s",
            session_create.id,
            session_create.session_date,
        )
    except IntegrityError as e:
        logger.info(
            "Session id=%s already exists, skipping creation", session_create.id
        )

    car_data = {
        "session_id": session_create.id,
        "car_id": session_create.car_id,
        "car_name": session_create.car_name,
        "car_class": session_create.car_class,
    }

    try:
        session_car = session_car_crud.create(db, car_data)
        logger.info(
            "Creating car for session with id=%s date=%s",
            session_create.car_id,
            session_create.session_date,
        )
    except IntegrityError as e:
        logger.error("Duplciate car creation failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Car with id {session_create.car_id} already exists for session with id {session_create.id}",
        )

    return session_car


@router.get("/{session_id}/cars/{car_id}/summary", response_model=RaceReport)
def get_race_summary(car: SessionCarDep, db: DbSessionDep):
    return generate_race_summary(car, db)
