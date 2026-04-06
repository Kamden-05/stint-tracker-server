from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.stint_model import Stint
    from app.models.session_model import SessionCar


class PitStop(Base):
    __tablename__ = "pit_stop"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int]
    car_id: Mapped[int]

    __table_args__ = ForeignKeyConstraint(
        ["session_id", "car_id"],
        ["session_car.session_id", "session_car.car_id"],
        ondelete="CASCADE",
    )
    
    session_car: Mapped["SessionCar"] = relationship(back_populates="pit_stops")

    road_enter_time: Mapped[float]
    service_start_time: Mapped[float]
    fuel_start_amount: Mapped[float]
    fuel_end_amount: Mapped[Optional[float]]
    required_repair_time: Mapped[float]
    optional_repair_time: Mapped[float]
    left_front_tire_change: Mapped[bool]
    left_rear_tire_change: Mapped[bool]
    right_front_tire_change: Mapped[bool]
    right_rear_tire_change: Mapped[bool]
    service_end_time: Mapped[Optional[float]]
    road_exit_time: Mapped[Optional[float]]

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
