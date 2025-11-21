from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.pit_schemas import PitRead, PitCreate, PitUpdate

from app.database.db import get_db
from app.models.stint_model import Stint
from app.models.pitstop_model import PitStop
from app.repositories import pit_crud, stint_crud

router = APIRouter(tags=["pits"])

DbSession = Annotated[Session, Depends(get_db)]

''' Nested Routes '''

@router.get("/stints/{stint_id}/pits", response_model=PitRead)
def get_pit_for_stint(stint_id: int, db: DbSession):
    pit = pit_crud.get_one(db, PitStop.stint_id == stint_id)

    if pit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Pit Stop with stint id {stint_id} not found'
        )
    
    return pit

@router.post("/stints/{stint_id}/pits", response_model=PitRead)
def create_pit(stint_id: int, pit_create: PitCreate, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)

    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Stint with id {stint_id} not found'
        )
    
    try:
        pit = pit_crud.create(db, pit_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Pit Stop with stint id {pit_create.stint_id} already exists",
        ) from e

    return pit

@router.patch("/pitstops/{pitstop_id}", response_model=PitRead)
def update_pit(pitstop_id: int, pit_update: PitUpdate, db: DbSession):
    pitstop = pit_crud.get_one(db, PitStop.id == pitstop_id)

    if pitstop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pitstop with id {pitstop_id} not found"
        )
    
    try:
        pitstop = pit_crud.update(db, pitstop, pit_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update pitstop with id {pitstop_id}. Error: {str(e)}",
        ) from e
    
    return pitstop


@router.get("/pits", response_model=list[PitRead])
def get_pitstops(db: DbSession):
    pits = pit_crud.get_many(db)
    return pits

@router.get("/pits", response_model=PitRead)
def get_pitstops_for_session(session_id: int, db: DbSession):
    pass

@router.get("/pits/{pit_id}", response_model=PitRead)
def get_pitstop(pit_id: int, db: DbSession):
    pit = pit_crud.get_one(db, PitStop.id == pit_id)

    if pit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pit Stop with id {pit_id} not found",
        )

    return pit
