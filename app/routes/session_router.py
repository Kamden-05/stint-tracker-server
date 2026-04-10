import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError

from app.dependencies import DbSessionDep, SessionCarDep, get_api_key
from app.models import Sessions, SessionCars
from app.repositories import session_car_crud, session_crud
from app.schemas import (
    RaceSessionCreate,
    RaceSessionRead,
    SessionCarRead,
    RaceReport,
)
from app.services import generate_race_summary, build_model

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
    dependencies=[Depends(get_api_key)],
)


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
    session = session_crud.get_one(db, Sessions.id == session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )

    return session


@router.post("", response_model=SessionCarRead)
def create_session(session_create: RaceSessionCreate, db: DbSessionDep):
    session = build_model(
        session_create,
        Sessions,
        exclude={"car_id", "car_name", "car_class"},
    )

    try:
        session_crud.create(db, session)
        logger.info(
            "Creating session for id=%s date=%s",
            session_create.id,
            session_create.session_date,
        )
    except IntegrityError:
        logger.info(
            "Session id=%s already exists, skipping creation", session_create.id
        )

    session_car = SessionCars(
        session_id=session_create.id,
        car_id=session_create.car_id,
        car_name=session_create.car_name,
        car_class=session_create.car_class,
    )

    try:
        session_car = session_car_crud.create(db, session_car)
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
        ) from e

    return session_car


@router.get("/{session_id}/cars/{car_id}/summary", response_model=RaceReport)
def get_race_summary(car: SessionCarDep, db: DbSessionDep):
    return generate_race_summary(car, db)
