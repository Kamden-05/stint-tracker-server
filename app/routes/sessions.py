from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from stint_core.session_base import RaceSession
from app.database.db import get_db
from typing import Annotated

router = APIRouter(prefix="/sessions", tags=["sessions"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/{session_id}", status_code=status.HTTP_201_CREATED)
def create_session(session: RaceSession, db: DbSession):
    pass
