# Stage 3: FastAPI + Persistence Silent Teacher
# Run:  pip install -r requirements_api.txt ; python test_api.py

import os

os.environ["DATABASE_URL"] = "sqlite:///test_congestion_history.db"

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# \u2500\u2500\u2500 /health \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
r = client.get("/health")
assert r.status_code == 200, f"/health returned {r.status_code}"
assert r.json()["status"] == "ok"

# \u2500\u2500\u2500 valid /calculate \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
demo = {
    "hourly_wage": 500,
    "normal_commute_mins": 35,
    "actual_commute_mins": 80,
    "work_days_per_year": 240,
}
r = client.post("/calculate", json=demo)
assert r.status_code == 200, f"/calculate returned {r.status_code}: {r.text}"
body = r.json()
assert body["annual_lost_hours"] > 0, "annual_lost_hours should be positive"
assert body["annual_financial_loss"] > 0
assert "exceeds_city_average" in body

# --- history persistence ---
r = client.get("/history")
assert r.status_code == 200, f"/history returned {r.status_code}: {r.text}"
history = r.json()
assert len(history) >= 1, "history should contain at least one saved calculation"
assert "annual_financial_loss" in history[0], "history item missing expected field"

r = client.get("/history?limit=1")
assert r.status_code == 200
assert len(r.json()) == 1, "limit parameter should restrict response size"

# \u2500\u2500\u2500 validation guard \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
bad = {**demo, "hourly_wage": -10}
r = client.post("/calculate", json=bad)
assert r.status_code == 422, "negative wage should be rejected with 422"

print("\u2705 Stage 3 complete: API is validated and calculation history is persisted!")
