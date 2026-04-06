from fastapi import APIRouter, HTTPException, status
from app.schemas.pit_schemas import PitRead, PitCreate, PitUpdate

from app.models.pitstop_model import PitStop
from app.repositories import pit_crud, stint_crud
from app.dependencies import DbSessionDep, SessionCarDep

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sessions/{session_id}/cars/{car_id}/pitstops", tags=["pitstops"]
)


@router.get("", response_model=list[PitRead])
def get_car_pitstops_for_session(car: SessionCarDep):
    return sorted(car.pit_stops, key=lambda p: p.road_enter_time)


@router.post(
    "",
    response_model=PitRead,
    response_model_exclude_none=True,
)
def create_pit(car: SessionCarDep, pit_create: PitCreate, db: DbSessionDep):
    pit_data = pit_create.model_dump()
    pit_data["session_id"] = car.session_id
    pit_data["car_id"] = car.car_id

    try:
        pitstop = pit_crud.create(db, pit_data)
        logger.info(
            "Created pitstop %s for session %s car %s",
            pitstop.id,
            car.session_id,
            car.car_id,
        )
    except Exception as e:
        logger.error("Failed to create pitstop: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't create pitstop. Error: {str(e)}",
        ) from e

    return pitstop


@router.patch("", response_model=PitRead)
def update_pit(car: SessionCarDep, pit_update: PitUpdate, db: DbSessionDep):
    pitstops = pit_crud.get_many(
        db,
        PitStop.session_id == car.session_id,
        PitStop.car_id == car.car_id,
        PitStop.road_exit_time == None,
    )

    if not pitstops:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No open pitstops found for session {car.session_id} and car {car.car_id}",
        )

    open_pitstops_sorted = sorted(pitstops, key=lambda p: p.road_enter_time)
    latest_pitstop = open_pitstops_sorted[-1]

    if len(open_pitstops_sorted) > 1:
        logger.warning("Multiple open pitstops found")

    try:
        updated_pitstop = pit_crud.update(db, latest_pitstop, pit_update)
        logger.info(
            "Updated pitstop %s for session %s car %s",
            latest_pitstop.id,
            car.session_id,
            car.car_id,
        )
    except Exception as e:
        logger.error("Failed to update stint: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update stint. Error: {str(e)}",
        ) from e

    return updated_pitstop
