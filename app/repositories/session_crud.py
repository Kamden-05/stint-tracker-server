from app.repositories.base_crud import CRUDRepository
from app.models.session_model import RaceSession

session_crud = CRUDRepository(model=RaceSession)
