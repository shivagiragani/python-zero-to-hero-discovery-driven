from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Calculation(Base):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hourly_wage: Mapped[float] = mapped_column(Float, nullable=False)
    normal_commute_mins: Mapped[float] = mapped_column(Float, nullable=False)
    actual_commute_mins: Mapped[float] = mapped_column(Float, nullable=False)
    work_days_per_year: Mapped[int] = mapped_column(Integer, nullable=False)

    daily_lost_hours: Mapped[float] = mapped_column(Float, nullable=False)
    annual_lost_hours: Mapped[float] = mapped_column(Float, nullable=False)
    annual_lost_days: Mapped[float] = mapped_column(Float, nullable=False)
    annual_financial_loss: Mapped[float] = mapped_column(Float, nullable=False)
    exceeds_city_average: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
