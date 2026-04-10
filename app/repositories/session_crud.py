from app.repositories.base_crud import CRUDRepository
from app.models.session_model import Sessions

session_crud = CRUDRepository(model=Sessions)
