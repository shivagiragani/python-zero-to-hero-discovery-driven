# ─── Silent Teacher ──────────────────────────────────────────────────────────
from fastapi.testclient import TestClient
from main import app, _tasks

_tasks.clear()          # reset state before test
client = TestClient(app)

r = client.get("/health")
assert r.status_code == 200
assert r.json()["status"] == "ok"

r = client.post("/tasks", json={"title": "Learn FastAPI"})
assert r.status_code == 201
assert r.json()["title"] == "Learn FastAPI"

r = client.get("/tasks")
assert r.status_code == 200
assert len(r.json()) == 1

print("\u2705 Lesson 6 complete: Service Counter mastered!")
