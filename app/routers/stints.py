from fastapi import APIRouter, FastAPI
from stint_core.stint_base import Stint

router = APIRouter(prefix='/stints')

@router.post("/")
def create_stint(race_id: int, stint: Stint):
    print(race_id)
    return stint

@router.post("/{stint_id}/update")
def update_stint(stint: Stint):
    return stint

@router.post("/{stint_id}/end")
def end_stint(stint: Stint):
    return stint