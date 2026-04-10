import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.dependencies import DbSessionDep, SessionCarDep, get_api_key
from app.models import Stints, Laps
from app.repositories import lap_crud, stint_crud
from app.schemas.lap_schemas import LapCreate, LapRead
from app.services import build_model

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["laps"],
    dependencies=[Depends(get_api_key)],
)


def get_stint(stint_id: int, db: DbSessionDep) -> Stints:
    stint = stint_crud.get_one(db, Stints.id == stint_id)

    if stint is None:
        logger.warning("Stint id=%s not found", stint_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


StintDep = Annotated[Stints, Depends(get_stint)]


@router.get("/stints/{stint_id}/laps", response_model=list[LapRead])
def get_laps_for_stint(stint: StintDep):
    return sorted(stint.laps, key=lambda l: l.number)


@router.get("/sessions/{session_id}/cars/{car_id}/laps", response_model=list[LapRead])
def get_car_laps_for_session(car: SessionCarDep, db: DbSessionDep):
    stints = stint_crud.get_many(
        db, Stints.session_id == car.session_id, Stints.car_id == car.car_id
    )

    laps = [lap for s in stints for lap in s.laps]

    return sorted(laps, key=lambda l: l.number)


@router.post("/stints/{stint_id}/laps", response_model=LapRead)
def create_lap(lap_create: LapCreate, stint: StintDep, db: DbSessionDep):
    try:
        lap = build_model(
            lap_create,
            Laps,
            stint_id=stint.id,
            session_id=stint.session_id,
            car_id=stint.car_id,
        )
        lap = lap_crud.create(db, lap)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Lap {lap_create.number} already exists for stint {stint.id}",
        ) from e

    return lap
