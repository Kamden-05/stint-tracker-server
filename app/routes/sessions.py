from fastapi import APIRouter, FastAPI
from stint_core.stint_base import Session

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/{session_id}")
def create_session(session_id: int, session: Session):

    return session


@router.put("/{session_id}/update/{stint_id}")
def update_session(session_id: int, session: Session):
    return session


@router.put("/{session_id}/end/{stint_id}")
def end_session(session_id: int, session: Session):
    return session
