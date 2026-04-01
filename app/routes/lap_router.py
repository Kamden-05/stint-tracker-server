from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.lap_schemas import LapRead, LapCreate
from app.database.db import get_db
from app.repositories import stint_crud, lap_crud
from app.models.stint_model import Stint
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stints/{stint_id}/laps", tags=["laps"])

DbSession = Annotated[Session, Depends(get_db)]


def get_stint(stint_id: int, db: DbSession) -> Stint:
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        logger.warning("Stint id=%s not found", stint_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


StintDep = Annotated[Stint, Depends(get_stint)]


@router.post("", response_model=LapRead)
def create_lap(lap_create: LapCreate, db: DbSession, stint: StintDep):

    try:
        lap = lap_crud.create(db, lap_create)
        logger.info("Created lap number %s for stint %s", lap_create.number, stint.id)
    except IntegrityError as e:
        logger.error(
            "Lap number %s already exists for stint %s", lap_create.number, stint.id
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Lap with lap number {lap_create.number} already exists",
        ) from e
    return lap


@router.get("", response_model=list[LapRead])
def get_laps_for_stint(stint: StintDep):
    return sorted(stint.laps, key=lambda l: l.number)
