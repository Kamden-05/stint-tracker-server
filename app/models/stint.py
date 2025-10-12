from sqlalchemy import ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from app.database.base_class import Base

if TYPE_CHECKING:
    from .lap import Lap
    from .session import Session

class Stint(Base):
    __tablename__ = "stint"

    stint_id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"))
    session: Mapped['Session'] = relationship(back_populates='session')
    laps: Mapped[List['Lap']] = relationship(back_populates='lap')
    driver_name: Mapped[str] = mapped_column(String)
    start_time: Mapped[float]
    length: Mapped[Optional[float]]
    laps_completed: Mapped[int]
    avg_lap: Mapped[Optional[float]]
    fastest_lap: Mapped[Optional[float]]
    out_lap: Mapped[Optional[float]]
    in_lap: Mapped[Optional[float]]
    start_position: Mapped[int]
    end_position: Mapped[Optional[int]]
    start_fuel: Mapped[float]
    end_fuel: Mapped[Optional[float]]
    refuel_amount: Mapped[Optional[float]]
    tire_change: Mapped[Optional[bool]]
    repairs: Mapped[Optional[bool]]
    pit_service_duration: Mapped[Optional[float]]
    incidents: Mapped[Optional[int]]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
