import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependencies.db_session import DbSessionDep
from app.models.session_model import SessionCars
from app.repositories import session_car_crud

logger = logging.getLogger(__name__)


def get_session_car(session_id: int, car_id: int, db: DbSessionDep) -> SessionCars:
    car = session_car_crud.get_one(
        db, SessionCars.session_id == session_id, SessionCars.car_id == car_id
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


SessionCarDep = Annotated[SessionCars, Depends(get_session_car)]
