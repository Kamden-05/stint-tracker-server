from app.repositories.base_crud import CRUDRepository
from app.models.session_model import Session

session_crud = CRUDRepository(model=Session)
