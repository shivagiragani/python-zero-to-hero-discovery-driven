from __future__ import annotations

import os
from typing import Iterator

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Calculation

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///congestion_history.db")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def save_calculation(session: Session, payload: dict, result: dict) -> Calculation:
    record = Calculation(
        hourly_wage=payload["hourly_wage"],
        normal_commute_mins=payload["normal_commute_mins"],
        actual_commute_mins=payload["actual_commute_mins"],
        work_days_per_year=payload["work_days_per_year"],
        daily_lost_hours=result["daily_lost_hours"],
        annual_lost_hours=result["annual_lost_hours"],
        annual_lost_days=result["annual_lost_days"],
        annual_financial_loss=result["annual_financial_loss"],
        exceeds_city_average=result["exceeds_city_average"],
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def list_recent_calculations(session: Session, limit: int = 10) -> list[Calculation]:
    stmt = select(Calculation).order_by(Calculation.id.desc()).limit(limit)
    return list(session.execute(stmt).scalars().all())
