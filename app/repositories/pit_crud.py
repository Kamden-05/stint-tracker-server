from app.repositories.base_crud import CRUDRepository
from app.models.pitstop_model import PitStop

pit_crud = CRUDRepository(model=PitStop)
