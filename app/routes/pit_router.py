from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.schemas.pit_schemas import PitRead, PitCreate, PitUpdate

from app.models.stint_model import Stint
from app.models.pitstop_model import PitStop
from app.repositories import pit_crud, stint_crud
from app.dependencies import DbSessionDep, SessionCarDep

import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["pitstops"])

""" Nested Routes """


@router.get("/stints/{stint_id}/pitstops", response_model=PitRead)
def get_pit_for_stint(stint_id: int, db: DbSessionDep):
    pit = pit_crud.get_one(db, PitStop.stint_id == stint_id)

    if pit is None:
        logger.warning("No pit stop found for stint id=%s", stint_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pit Stop with stint id {stint_id} not found",
        )

    return pit


@router.post("/stints/{stint_id}/pitstops", response_model=PitRead)
def create_pit(stint_id: int, pit_create: PitCreate, db: DbSessionDep):
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    try:
        pit = pit_crud.create(db, pit_create)
        logger.info("Create pit stop for stint %s", stint.id)
    except IntegrityError as e:
        logger.error("Pit stop already exists for stint %s", stint.id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Pit Stop with stint id {pit_create.stint_id} already exists",
        ) from e

    return pit


@router.patch("/pitstops/{pitstop_id}", response_model=PitRead)
def update_pit(pitstop_id: int, pit_update: PitUpdate, db: DbSessionDep):
    pitstop = pit_crud.get_one(db, PitStop.id == pitstop_id)

    if pitstop is None:
        logger.warning("No pit stop found for id=%s", pitstop_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pitstop with id {pitstop_id} not found",
        )

    try:
        pitstop = pit_crud.update(db, pitstop, pit_update)
    except Exception as e:
        logger.error("Failed to update pit stop with id=%s", pitstop_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update pitstop with id {pitstop_id}. Error: {str(e)}",
        ) from e

    return pitstop


@router.get("/pitstops", response_model=list[PitRead])
def get_pitstops(db: DbSessionDep):
    pits = pit_crud.get_many(db)
    logger.info("Retrieved %d pit stops", len(pits))
    return pits


@router.get("/pitstops/session/{session_id}", response_model=list[PitRead])
def get_pitstops_for_session(session_id: int, db: DbSessionDep):
    stints = stint_crud.get_many(db, Stint.session_id == session_id)

    pits = [stint.pit_stop for stint in stints if stint.pit_stop is not None]

    if not pits:
        logger.info("No pit stops found for session id=%s", session_id)
        return []

    logger.info("Retrieved %d pit stops for session id=%s", len(pits), session_id)
    return pits


@router.get("/pitstops/{pit_id}", response_model=PitRead)
def get_pitstop(pit_id: int, db: DbSessionDep):
    pit = pit_crud.get_one(db, PitStop.id == pit_id)

    if pit is None:
        logger.warning("No pit stop found for id=%s", pit_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pit Stop with id {pit_id} not found",
        )

    return pit
