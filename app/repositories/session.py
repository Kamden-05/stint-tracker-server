from app.repositories.base import CRUDRepository
from app.models.session import Session

session_crud = CRUDRepository(model=Session)
