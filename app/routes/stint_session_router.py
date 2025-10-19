from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.stint_schemas import StintCreate, StintUpdate, StintRead

from app.database.db import get_db
from app.models.session_model import Session as Session
from app.models.stint_model import Stint
from app.repositories import session_crud, stint_crud

router = APIRouter(prefix="/sessions/{session_id}/stints", tags=["session_stints"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/{stint_id}", response_model=StintRead)
def get_stint(session_id: int, stint_id: int, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)
    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


@router.get("/", response_model=list[StintRead])
def get_stints_for_session(session_id: int, db: DbSession):
    session = session_crud.get_one(db, Session.id == session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with {session_id} not found",
        )

    return session.stints


@router.post("/")
def create_stint(session_id: int, stint_create: StintCreate, db: DbSession):
    session = session_crud.get_one(db, Session.id == session_id)

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
            detail=f"Stint with stint number {stint_create.number} already exists",
        ) from e

    return stint
