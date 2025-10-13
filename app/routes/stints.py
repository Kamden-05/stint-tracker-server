from fastapi import APIRouter, Depends, HTTPException, status
from stint_core.stint_base import StintCreate, StintUpdate
from app.database.db import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.repositories import stint_crud, session_crud
from app.models.session import Session as RaceSession


router = APIRouter(prefix="/sessions/{session_id}/stints", tags=["stints"])

DbSession = Annotated[Session, Depends(get_db)]

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
