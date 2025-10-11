from fastapi import APIRouter

router = APIRouter(
    prefix='/stints'
    tags=['Stints']
)

@router.post("/")
def create_stint(stint: StintCreate)