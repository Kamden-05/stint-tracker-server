from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.stint_base import StintCreate, StintUpdate

from app.database.db import get_db
from app.models.session_model import Session as RaceSession
from app.models.stint_model import Stint
from app.repositories import session_crud, stint_crud

router = APIRouter(prefix="/sessions/{session_id}/stints", tags=["stints"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/{stint_id}")
def get_stint(session_id: int, stint_id: int, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)
    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


@router.post("/")
def create_stint(session_id: int, stint_create: StintCreate, db: DbSession):
    session = session_crud.get_one(db, RaceSession.id == session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )
    try:
        stint = stint_crud.create(db, stint_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Stint with stint number {stint_create.stint_number} already exists",
        ) from e

    return stint


@router.put("/{stint_id}")
def update_stint(stint_id: int, stint_update: StintUpdate, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    try:
        stint = stint_crud.update(db, stint, stint_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update stint with id {stint_id}. Error: {str(e)}",
        ) from e

    return stint
