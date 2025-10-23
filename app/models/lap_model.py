from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy import func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.stint_model import Stint


class Lap(Base):
    __tablename__ = "lap"

    id: Mapped[int] = mapped_column(primary_key=True)
    stint_id: Mapped[int] = mapped_column(ForeignKey("stint.id", ondelete='CASCADE'))
    stint: Mapped["Stint"] = relationship(back_populates="laps")
    number: Mapped[int]
    time: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('stint_id', 'number', name='unique_lap_per_stint'),
    )