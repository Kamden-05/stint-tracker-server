from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.pit_schemas import PitRead

from app.database.db import get_db
from app.models.pitstop_model import PitStop
from app.repositories import pit_crud

router = APIRouter(prefix="/pitstops", tags=["pitstops"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[PitRead])
def get_pitstops(db: DbSession):
    pits = pit_crud.get_many(db)
    return pits


@router.get("/{pit_id}", response_model=PitRead)
def get_pitstop(pit_id: int, db: DbSession):
    pit = pit_crud.get_one(db, PitStop.id == pit_id)

    if pit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pit Stop with id {pit_id} not found",
        )

    return pit
