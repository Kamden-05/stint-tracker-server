from app.repositories.base_crud import CRUDRepository
from app.models.lap_model import Lap
from sqlalchemy import select
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


lap_crud = CRUDRepository(model=Lap)


def get_many(
    self, db: Session, *args, skip: int = 0, limit: int = 100, **kwargs
) -> list[Lap]:
    logger.debug(
        f"Retrieving records for {self.model.__name__} with skip {skip} and limit {limit}"
    )
    filters = [
        *args,
        *[getattr(self.model, k) == v for k, v in kwargs.items() if v is not None],
    ]
    stmt = (
        select(self.model)
        .where(*filters)
        .order_by(Lap.number)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()
