from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from stint_core.lap_base import LapCreate
from app.database.db import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.repositories import stint_crud, lap_crud
from app.models.stint import Stint
from app.services.sheets_service import update_range

router = APIRouter(prefix='/stints/{stint_id}/laps', tags=['laps'])

DbSession = Annotated[Session, Depends(get_db)]

@router.post("/")
def create_lap(stint_id: int, lap_create: LapCreate, db: DbSession, background_tasks: BackgroundTasks, sheet_id: str = None, sheet_range: str = None):
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Stint with id {stint_id} not found'
        )
    
    try:
        lap = lap_crud.create(db, lap_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Lap with lap number {lap_create.lap_number} already exists'
        ) from e
    
    if sheet_id is not None:
        background_tasks.add_task(update_range, sheet_id, sheet_range, stint.laps)
    return lap