from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.stint_schemas import StintCreate, StintRead

from app.database.db import get_db
from app.models.session_model import Session as RaceSession
from app.models.stint_model import Stint
from app.repositories import session_crud, stint_crud

router = APIRouter(tags=["stints"])

DbSession = Annotated[Session, Depends(get_db)]

''' Nested Routes'''

@router.get("/sessions/{session_id}/stints/latest", response_model=StintRead)
def get_latest_stint(session_id: int, db: DbSession):
    session = session_crud.get_one(db, RaceSession.id == session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )

    if len(session.stints) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Session with id {session_id} has no stints",
        )

    return session.stints[-1]


@router.get("/sessions/{session_id}/number/{stint_number}", response_model=StintRead)
def get_stint_by_number(session_id: int, stint_number: int, db: DbSession):
    stint = stint_crud.get_one(
        db, Stint.number == stint_number, Stint.session_id == session_id
    )
    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint number {stint_number} not found",
        )

    return stint

@router.get("/sessions/{session_id}/stints", response_model=list[StintRead])
def get_stints_for_session(session_id: int, db: DbSession):
    session = session_crud.get_one(db, RaceSession.id == session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with {session_id} not found",
        )

    return session.stints


@router.post("/sessions/{session_id}/stints", response_model=StintRead, response_model_exclude_none=True)
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
            detail=f"Stint with stint number {stint_create.number} already exists",
        ) from e

    return stint


''' Flat Routes '''

@router.get("/stints", response_model=list[StintRead])
def get_stints(db: DbSession):
    stints = stint_crud.get_many(db)
    return stints


@router.get("/stints/{stint_id}", response_model=StintRead)
def get_stint(stint_id: int, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)
    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


@router.put("/stints/{stint_id}", response_model=StintRead)
def update_stint(stint_id: int, stint_update: StintUpdate, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    if stint.is_complete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Stint with id {stint_id} can no longer be updated",
        )

    try:
        stint = stint_crud.update(db, stint, stint_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update stint with id {stint_id}. Error: {str(e)}",
        ) from e

    return stint
