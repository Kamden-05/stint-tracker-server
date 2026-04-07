from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy import func, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.stint_model import Stint
    from app.models.session_model import SessionCar


class Lap(Base):
    __tablename__ = "lap"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int]
    car_id: Mapped[int]

    __table_args__ = (
        ForeignKeyConstraint(
            ["session_id", "car_id"],
            ["session_car.session_id", "session_car.car_id"],
            ondelete="CASCADE",
        ),
        UniqueConstraint(
        "stint_id", "number", name="unique_stint_lap_number"
        ),
    )
    stint_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stint.id", ondelete="SET NULL")
    )
    session_car: Mapped["SessionCar"] = relationship(back_populates="laps")
    stint: Mapped["Stint"] = relationship(back_populates="laps")
    number: Mapped[int]
    lap_time: Mapped[float]
    end_time: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
