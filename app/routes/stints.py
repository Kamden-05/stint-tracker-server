from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from stint_core.stint_base import StintCreate, StintUpdate

from app.database.db import get_db
from app.models.session import Session as RaceSession
from app.models.stint import Stint
from app.repositories import session_crud, stint_crud
from app.services.sheets_service import update_range

router = APIRouter(prefix="/sessions/{session_id}/stints", tags=["stints"])

DbSession = Annotated[Session, Depends(get_db)]

@router.post("/")
def create_stint(
    session_id: int,
    stint_create: StintCreate,
    db: DbSession,
    background_tasks: BackgroundTasks,
    sheet_id: str = None,
    sheet_range: str = None,
):
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

    if sheet_id is not None:
        stint_data = stint_create.model_dump()
        sheet_data = [list(stint_data.keys()), list(stint_data.values())]
        background_tasks.add_task(update_range, sheet_id, sheet_range, sheet_data)
    return stint


@router.put("/{stint_id}")
def update_stint(
    stint_id: int,
    stint_update: StintUpdate,
    db: DbSession,
    background_tasks: BackgroundTasks,
    sheet_id: str = None,
    sheet_range: str = None,
):
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

    if sheet_id is not None:
        stint_data = stint_update.model_dump()
        sheet_data = [list(stint_data.keys()), list(stint_data.values())]

        background_tasks.add_task(update_range, sheet_id, sheet_range, sheet_data)
    return stint
