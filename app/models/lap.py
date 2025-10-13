from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .stint import Stint


class Lap(Base):
    __tablename__ = "lap"

    id: Mapped[int] = mapped_column(primary_key=True)
    stint_id: Mapped[int] = mapped_column(ForeignKey("stint.id"))
    stint: Mapped["Stint"] = relationship(back_populates="laps")
    number: Mapped[int]
    time: Mapped[float]
    incidents: Mapped[Optional[int]]
    start_position: Mapped[Optional[int]]
    end_position: Mapped[Optional[int]]
    pit: Mapped[Optional[bool]]
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
