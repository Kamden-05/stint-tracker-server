from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from . import BaseModel

if TYPE_CHECKING:
    from .stint import Stint

class Lap(BaseModel):
    __tablename__ = "lap"

    lap_id: Mapped[int] = mapped_column(primary_key=True)
    stint_id: Mapped[int] = mapped_column(ForeignKey("stint.stint_id"))
    stint: Mapped['Stint'] = relationship(back_populates='laps')
    number: Mapped[int]
    time: Mapped[float]
    incidents: Mapped[Optional[int]]
    start_position: Mapped[Optional[int]]
    end_position: Mapped[Optional[int]]
    pit: Mapped[Optional[bool]]
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
