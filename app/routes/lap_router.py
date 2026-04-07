from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.schemas.lap_schemas import LapRead, LapCreate
from app.repositories import stint_crud, lap_crud
from app.models import Stint
from app.dependencies import SessionCarDep, DbSessionDep
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["laps"])


def get_stint(stint_id: int, db: DbSessionDep) -> Stint:
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        logger.warning("Stint id=%s not found", stint_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


StintDep = Annotated[Stint, Depends(get_stint)]


@router.get("/stints/{stint_id}/laps", response_model=list[LapRead])
def get_laps_for_stint(stint: StintDep):
    return sorted(stint.laps, key=lambda l: l.number)


@router.get("/sessions/{session_id}/cars/{car_id}/laps", response_model=list[LapRead])
def get_car_laps_for_session(car: SessionCarDep, db: DbSessionDep):
    stints = stint_crud.get_many(
        db, Stint.session_id == car.session_id, Stint.car_id == car.car_id
    )

    laps = [lap for s in stints for lap in s.laps]

    return sorted(laps, key=lambda l: l.number)


@router.post("/stints/{stint_id}/laps", response_model=LapRead)
def create_lap(lap_create: LapCreate, stint: StintDep, db: DbSessionDep):
    try:
        lap_data = lap_create.model_dump()
        lap_data["stint_id"] = stint.id
        lap_data["session_id"] = stint.session_id
        lap_data["car_id"] = stint.car_id
        lap = lap_crud.create(db, lap_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Lap {lap_create.number} already exists for stint {stint.id}",
        )

    return lap
