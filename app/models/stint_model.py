from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, String, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models import SessionCars, Laps


class Stints(Base):
    __tablename__ = "stints"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int]
    car_id: Mapped[int]

    __table_args__ = (
        ForeignKeyConstraint(
            ["session_id", "car_id"],
            ["session_cars.session_id", "session_cars.car_id"],
            ondelete="CASCADE",
        ),
    )
    session_car: Mapped["SessionCars"] = relationship(back_populates="stints")

    laps: Mapped[List["Laps"]] = relationship(
        back_populates="stint", order_by="Laps.end_time"
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

    # pylint: disable=not-callable
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
