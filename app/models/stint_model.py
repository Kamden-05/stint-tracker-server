from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, ForeignKey, String, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.lap_model import Lap
    from app.models.session_model import SessionCar
    from app.models.pitstop_model import PitStop


class Stint(Base):
    __tablename__ = "stint"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int]
    car_id: Mapped[int]

    __table_args__ = ForeignKeyConstraint(
        ["session_id", "car_id"],
        ["session_car.session_id", "session_car.car_id"],
        ondelete="CASCADE",
    )
    session_car: Mapped["SessionCar"] = relationship(back_populates="stints")

    laps: Mapped[List["Lap"]] = relationship(
        back_populates="stint", order_by="Lap.start_time"
    )

    driver_name: Mapped[str] = mapped_column(String)
    start_time: Mapped[float]
    start_position: Mapped[int]
    start_incidents: Mapped[int]
    start_fuel: Mapped[float]
    end_time: Mapped[Optional[float]]
    end_position: Mapped[Optional[int]]
    end_fuel: Mapped[Optional[float]]
    end_incidents: Mapped[Optional[int]]
    track_temp: Mapped[float]
    track_wetness: Mapped[int]
    sky_cover: Mapped[int]
    precipitation: Mapped[float]

    is_complete: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
