from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.stint_schemas import StintRead, StintUpdate

from app.database.db import get_db
from app.models.stint_model import Stint
from app.repositories import stint_crud

router = APIRouter(prefix="/stints", tags=["stints"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[StintRead])
def get_stints(db: DbSession):
    stints = stint_crud.get_many(db)
    return stints


@router.get("/{stint_id}", response_model=StintRead)
def get_stint(stint_id: int, db: DbSession):
    stint = stint_crud.get_one(db, Stint.id == stint_id)
    if stint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {stint_id} not found",
        )

    return stint


@router.put("/{stint_id}", response_model=StintRead)
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
