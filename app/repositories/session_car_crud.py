from app.repositories.base_crud import CRUDRepository
from app.models.session_model import SessionCars

session_car_crud = CRUDRepository(model=SessionCars)
