from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.stint_schemas import StintCreate, StintRead, StintUpdate

from app.database.db import get_db
from app.models.session_model import SessionCar
from app.models.stint_model import Stint
from app.repositories import session_car_crud, stint_crud

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sessions/{session_id}/cars/{car_id}/stints", tags=["stints"]
)

DbSession = Annotated[Session, Depends(get_db)]


def get_session_car(session_id: int, car_id: int, db: DbSession) -> SessionCar:
    car = session_car_crud.get_one(
        db, SessionCar.session_id == session_id, SessionCar.car_id == car_id
    )

    if not car:
        logger.warning(
            "Session not found with session_id=%s, car_id=%s", session_id, car_id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car id={car_id} not found in session with id {session_id}",
        )

    return car


SessionCarDep = Annotated[SessionCar, Depends(get_session_car)]

""" Nested Routes"""


@router.get("", response_model=list[StintRead])
def get_car_stints_for_session(car: SessionCarDep):
    return sorted(car.stints, key=lambda s: s.start_time)


@router.post(
    "",
    response_model=StintRead,
    response_model_exclude_none=True,
)
def create_stint(
    car: SessionCarDep,
    stint_create: StintCreate,
    db: DbSession,
):
    if stint_create.session_id != car.session_id or stint_create.car_id != car.car_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID or Car ID in request body does not match URL",
        )
    stint = stint_crud.create(db, stint_create)
    logger.info(
        "Created stint %s for session %s car %s", stint.id, car.session_id, car.car_id
    )

    return stint


@router.patch("/{stint_id}", response_model=StintRead)
def update_stint(
    stint_id: int, car: SessionCarDep, stint_update: StintUpdate, db: DbSession
):
    stint = stint_crud.get_one(
        db,
        Stint.id == stint_id,
        Stint.session_id == car.session_id,
        Stint.car_id == car.car_id,
    )

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint {stint_id} not found for session {car.session_id} and car {car.car_id}",
        )

    if stint.is_complete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Stint {stint_id} is complete and cannot be updated",
        )

    try:
        updated_stint = stint_crud.update(db, stint, stint_update)
        logger.info(
            "Updated stint %s for session %s car %s",
            stint.id,
            car.session_id,
            car.car_id,
        )
    except Exception as e:
        logger.error("Failed to update stint: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update stint. Error: {str(e)}",
        ) from e

    return updated_stint
