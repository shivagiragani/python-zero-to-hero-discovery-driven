from __future__ import annotations

from dataclasses import dataclass


DEFAULT_WORK_DAYS_PER_YEAR = 240
AVERAGE_BENGALURU_TRAFFIC_HOURS = 168


@dataclass(frozen=True)
class CongestionInput:
    hourly_wage: float
    normal_commute_mins: float
    actual_commute_mins: float
    work_days_per_year: int = DEFAULT_WORK_DAYS_PER_YEAR


@dataclass(frozen=True)
class CongestionResult:
    daily_lost_hours: float
    annual_lost_hours: float
    annual_lost_days: float
    annual_financial_loss: float
    exceeds_city_average: bool


def _validate_non_negative(name: str, value: float) -> float:
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")
    return value


def calculate_congestion_impact(user_input: CongestionInput) -> CongestionResult:
    hourly_wage = _validate_non_negative("Hourly wage", user_input.hourly_wage)
    normal_commute_mins = _validate_non_negative(
        "Normal commute minutes",
        user_input.normal_commute_mins,
    )
    actual_commute_mins = _validate_non_negative(
        "Actual commute minutes",
        user_input.actual_commute_mins,
    )

    if user_input.work_days_per_year <= 0:
        raise ValueError("Work days per year must be greater than zero.")

    extra_commute_mins = max(actual_commute_mins - normal_commute_mins, 0)
    daily_lost_hours = (extra_commute_mins * 2) / 60
    annual_lost_hours = daily_lost_hours * user_input.work_days_per_year
    annual_financial_loss = annual_lost_hours * hourly_wage

    return CongestionResult(
        daily_lost_hours=daily_lost_hours,
        annual_lost_hours=annual_lost_hours,
        annual_lost_days=annual_lost_hours / 24,
        annual_financial_loss=annual_financial_loss,
        exceeds_city_average=annual_lost_hours > AVERAGE_BENGALURU_TRAFFIC_HOURS,
    )


def build_cli_summary(result: CongestionResult) -> str:
    lines = [
        "--- Your Annual Impact ---",
        f"Time Lost: {result.annual_lost_hours:.1f} hours",
        f"Equivalent to: {result.annual_lost_days:.1f} full days stuck in traffic.",
        f"Financial 'Tax': Rs.{result.annual_financial_loss:,.2f} in lost productivity.",
    ]

    if result.exceeds_city_average:
        lines.append(
            "Alert: You are losing more than the Bengaluru average of 168 hours annually."
        )

    return "\n".join(lines)


def _prompt_float(prompt: str) -> float:
    return float(input(prompt).strip())


def _prompt_int_with_default(prompt: str, default: int) -> int:
    raw_value = input(prompt).strip()
    if not raw_value:
        return default
    return int(float(raw_value))


def run_cli() -> None:
    print("--- Bengaluru Personal Congestion Tax Calculator ---")

    user_input = CongestionInput(
        hourly_wage=_prompt_float("Enter your approximate hourly earnings (in Rs.): "),
        normal_commute_mins=_prompt_float(
            "How long should your commute take one-way? (mins): "
        ),
        actual_commute_mins=_prompt_float(
            "How long does it take during rush hour? (mins): "
        ),
        work_days_per_year=_prompt_int_with_default(
            "How many commute-heavy work days do you have per year? (default 240): ",
            DEFAULT_WORK_DAYS_PER_YEAR,
        ),
    )

    result = calculate_congestion_impact(user_input)
    print()
    print(build_cli_summary(result))


if __name__ == "__main__":
    run_cli()