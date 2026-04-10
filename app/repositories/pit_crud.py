from app.repositories.base_crud import CRUDRepository
from app.models.pitstop_model import PitStops

pit_crud = CRUDRepository(model=PitStops)
