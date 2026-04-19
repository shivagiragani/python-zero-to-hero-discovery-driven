<img width="1024" height="1024" alt="Bengaluru Congestion Tax Calculator" src="https://github.com/user-attachments/assets/8a614e2d-0142-40d6-acda-7a40919b8f12" />
# Bengaluru Congestion Tax Calculator

Estimate how much Bengaluru traffic costs a commuter in time and lost productivity.

This project started as a simple Python web app and now includes:

1. Core domain logic for congestion impact calculation.
2. A browser-based UI served from Python.
3. A FastAPI service layer.
4. SQLite-backed history persistence via SQLAlchemy.

## What The App Does

The calculator accepts:

1. Hourly wage in rupees.
2. Ideal one-way commute time.
3. Actual rush-hour one-way commute time.
4. Commute-heavy work days per year.

It returns:

1. Daily lost hours.
2. Annual lost hours.
3. Equivalent lost days.
4. Annual productivity loss in rupees.
5. Whether the loss is above the 168-hour Bengaluru benchmark.

## Tech Stack

1. Python 3.11+
2. FastAPI
3. SQLAlchemy
4. SQLite
5. Standard library HTTP server for the HTML UI
6. HTML + CSS

## Project Structure

1. `Calc_traffic.py`
   Core business logic, validation, dataclasses, and CLI summary helpers.
2. `app.py`
   Server-rendered browser UI using Python's built-in HTTP server.
3. `api.py`
   FastAPI service exposing `/health`, `/calculate`, and `/history`.
4. `db.py`
   Database engine, sessions, schema initialization, and persistence helpers.
5. `models.py`
   SQLAlchemy model for saved calculations.
6. `templates/index.html`
   HTML template used by the browser UI.
7. `static/styles.css`
   Styling for the browser UI.
8. `test_api.py`
   Silent-teacher integration test for API validation and persistence.
9. `requirements.txt`
   Main project dependencies.

## Run The Browser UI

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:8000
```

## Run The FastAPI Service

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the API:

```bash
uvicorn api:app --reload --port 8001
```

Open:

```text
http://127.0.0.1:8001/docs
```

## Environment

The database location is controlled by `DATABASE_URL`.

Default:

```text
sqlite:///congestion_history.db
```

Example for local development:

```bash
set DATABASE_URL=sqlite:///congestion_history.db
```

See `.env.example` for a sample value.

## API Endpoints

1. `GET /health`
   Returns service status and version.
2. `POST /calculate`
   Calculates congestion impact and saves the result to the database.
3. `GET /history?limit=10`
   Returns recent saved calculations.

## Example API Request

```json
{
  "hourly_wage": 500,
  "normal_commute_mins": 35,
  "actual_commute_mins": 80,
  "work_days_per_year": 240
}
```

## Example API Response

```json
{
  "daily_lost_hours": 1.5,
  "annual_lost_hours": 360.0,
  "annual_lost_days": 15.0,
  "annual_financial_loss": 180000.0,
  "exceeds_city_average": true,
  "benchmark_hours": 168,
  "benchmark_label": "Bengaluru city average"
}
```

## Run Tests

```bash
python test_api.py
```

The test verifies:

1. The API starts correctly.
2. `/health` responds successfully.
3. `/calculate` validates and computes correctly.
4. `/history` persists and returns calculation records.

## Suggested Screenshots For GitHub

1. Home page with form.
2. Calculated result cards and charts.
3. FastAPI Swagger docs page.
4. Example `/history` response.

## Future Improvements

1. Add a React frontend.
2. Add monthly and weekly impact breakdowns.
3. Add charts from saved history.
4. Add PostgreSQL deployment configuration.
5. Add end-to-end browser tests.

## Learning Value

This project demonstrates how to separate:

1. Business logic.
2. Presentation layer.
3. API layer.
4. Persistence layer.

That makes it useful both as a portfolio project and as a learning reference for Python-to-full-stack progression.
