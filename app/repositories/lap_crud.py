from app.repositories.base_crud import CRUDRepository
from app.models.lap_model import Lap

lap_crud = CRUDRepository(model=Lap)
