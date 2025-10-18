from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.lap_schemas import LapCreate
from app.database.db import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.repositories import stint_crud, lap_crud
from app.models.stint_model import Stint

router = APIRouter(prefix='/stints/{stint_id}/laps', tags=['laps'])

DbSession = Annotated[Session, Depends(get_db)]

@router.post("/")
def create_lap(stint_id: int, lap_create: LapCreate, db: DbSession):
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
    return lap