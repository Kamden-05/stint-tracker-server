from fastapi import APIRouter, FastAPI
from stint_core.stint_base import Stint

router = APIRouter(prefix="/stints")


@router.post("/{session_id}")
def create_stint(session_id: int, stint: Stint):

    return stint


@router.put("/{session_id}/update/{stint_id}")
def update_stint(session_id: int, stint: Stint):
    return stint


@router.put("/{session_id}/end/{stint_id}")
def end_stint(session_id: int, stint: Stint):
    return stint
