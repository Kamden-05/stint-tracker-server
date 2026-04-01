from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.stint_schemas import StintCreate, StintRead, StintUpdate

from app.database.db import get_db
from app.models.session_model import RaceSession
from app.models.stint_model import Stint
from app.repositories import session_crud, stint_crud

import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["stints"])

DbSession = Annotated[Session, Depends(get_db)]


def get_session(session_id: int, db: DbSession) -> RaceSession:
    session = session_crud.get_one(db, RaceSession.id == session_id)

    if not session:
        logger.warning("Session %s not found", session_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )

    return session


RaceSessionDep = Annotated[RaceSession, Depends(get_session)]

""" Nested Routes"""


@router.get("/sessions/{session_id}/stints/latest", response_model=StintRead)
def get_latest_stint(session: RaceSessionDep):

    if not session.stints:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Session with id {session.id} has no stints",
        )

    latest_stint = max(session.stints, key=lambda s: s.number)

    return latest_stint


@router.get("/sessions/{session_id}/number/{stint_number}", response_model=StintRead)
def get_stint_by_number(session: RaceSessionDep, stint_number: int, db: DbSession):
    stint = stint_crud.get_one(
        db, Stint.number == stint_number, Stint.session_id == session.id
    )

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint number {stint_number} not found",
        )

    return stint


@router.get("/sessions/{session_id}/stints", response_model=list[StintRead])
def get_stints_for_session(session: RaceSessionDep):
    return sorted(session.stints, key=lambda s: s.number)


@router.post(
    "/sessions/{session_id}/stints",
    response_model=StintRead,
    response_model_exclude_none=True,
)
def create_stint(session: RaceSessionDep, stint_create: StintCreate, db: DbSession):

    try:
        stint = stint_crud.create(db, stint_create)
        logger.info("Created stint %s for session %s", stint_create.number, session.id)
    except IntegrityError as e:
        logger.warning(
            "Failed to create stint %s for session %s: %s",
            stint_create.number,
            session.id,
            e,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Stint with stint number {stint_create.number} already exists",
        ) from e

    return stint


@router.get("/stints", response_model=list[StintRead])
def get_stints(db: DbSession):
    stints = stint_crud.get_many(db)
    return stints


@router.get("/stints/{stint_id}", response_model=StintRead)
def get_stint(stint_id: int, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)
    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


@router.patch("/stints/{stint_id}", response_model=StintRead)
def update_stint(stint_id: int, stint_update: StintUpdate, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    if stint.is_complete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Stint with id {stint_id} can no longer be updated",
        )

    try:
        stint = stint_crud.update(db, stint, stint_update)
        logger.info("Updated stint %s", stint_id)
    except Exception as e:
        logger.error("Failed to update stint %s: %s", stint_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update stint with id {stint_id}. Error: {str(e)}",
        ) from e

    return stint
