# \u2500\u2500\u2500 Stage 2: FastAPI Service Counter \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
# Discovery-driven analogy: A service counter placed *in front of* the existing engine.
# The engine (Calc_traffic.py) does not change \u2013 we only add a labelled counter.
#
# Run:   uvicorn api:app --reload --port 8001
# Docs:  http://127.0.0.1:8001/docs
# Note:  Existing HTTP server (app.py) runs on port 8000 \u2013 use 8001 here.

from __future__ import annotations

from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator

from Calc_traffic import (
    DEFAULT_WORK_DAYS_PER_YEAR,
    CongestionInput,
    calculate_congestion_impact,
)
from db import get_session, init_db, list_recent_calculations, save_calculation

app = FastAPI(
    title="Personal Congestion Tax API",
    description="FastAPI wrapper around the Bengaluru commute calculator.",
    version="0.2.0",
)

init_db()

# Allow React dev-server on port 3000 during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# \u2500\u2500\u2500 Request / Response schemas \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

class CalculateRequest(BaseModel):
    hourly_wage:          float = Field(gt=0,  description="Hourly earnings in Rs.")
    normal_commute_mins:  float = Field(ge=0,  description="Ideal one-way commute (minutes)")
    actual_commute_mins:  float = Field(ge=0,  description="Rush-hour one-way commute (minutes)")
    work_days_per_year:   int   = Field(
        default=DEFAULT_WORK_DAYS_PER_YEAR,
        gt=0,
        description="Working commute days per year",
    )

    @model_validator(mode="after")
    def actual_gte_normal(self) -> "CalculateRequest":
        if self.actual_commute_mins < self.normal_commute_mins:
            raise ValueError(
                "actual_commute_mins should be >= normal_commute_mins "
                "(rush hour is usually slower than ideal)."
            )
        return self


class CalculateResponse(BaseModel):
    daily_lost_hours:    float
    annual_lost_hours:   float
    annual_lost_days:    float
    annual_financial_loss: float
    exceeds_city_average: bool
    benchmark_hours:     int   = 168
    benchmark_label:     str   = "Bengaluru city average"


class HistoryItem(BaseModel):
    id: int
    hourly_wage: float
    normal_commute_mins: float
    actual_commute_mins: float
    work_days_per_year: int
    annual_lost_hours: float
    annual_financial_loss: float
    exceeds_city_average: bool


# \u2500\u2500\u2500 Routes \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

@app.get("/health", tags=["ops"])
def health():
    """Confirm the service counter is open."""
    return {"status": "ok", "version": app.version}


@app.post("/calculate", response_model=CalculateResponse, tags=["calculator"])
def calculate(
    payload: CalculateRequest,
    session: Annotated[Session, Depends(get_session)],
) -> CalculateResponse:
    """
    Post your commute profile and receive your annual congestion impact.

    Three-Period:
    - Observe: POST the default demo values and inspect the response body.
    - Explore: Change hourly_wage and watch annual_financial_loss scale.
    - Create:  Add a /calculate/monthly route that returns monthly equivalents.
    """
    try:
        result = calculate_congestion_impact(
            CongestionInput(
                hourly_wage=payload.hourly_wage,
                normal_commute_mins=payload.normal_commute_mins,
                actual_commute_mins=payload.actual_commute_mins,
                work_days_per_year=payload.work_days_per_year,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    response = CalculateResponse(
        daily_lost_hours=result.daily_lost_hours,
        annual_lost_hours=result.annual_lost_hours,
        annual_lost_days=result.annual_lost_days,
        annual_financial_loss=result.annual_financial_loss,
        exceeds_city_average=result.exceeds_city_average,
    )

    save_calculation(
        session=session,
        payload=payload.model_dump(),
        result=response.model_dump(),
    )

    return response


@app.get("/history", response_model=list[HistoryItem], tags=["calculator"])
def history(
    session: Annotated[Session, Depends(get_session)],
    limit: int = 10,
) -> list[HistoryItem]:
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 100")

    rows = list_recent_calculations(session=session, limit=limit)
    return [
        HistoryItem(
            id=row.id,
            hourly_wage=row.hourly_wage,
            normal_commute_mins=row.normal_commute_mins,
            actual_commute_mins=row.actual_commute_mins,
            work_days_per_year=row.work_days_per_year,
            annual_lost_hours=row.annual_lost_hours,
            annual_financial_loss=row.annual_financial_loss,
            exceeds_city_average=row.exceeds_city_average,
        )
        for row in rows
    ]

