# ─── Sandbox: The Service Counter (FastAPI) ──────────────────────────────────
# Analogy: Each route is a labeled counter at a service desk.
# You drop a request at the right counter and get a specific response.
#
# Run:  uvicorn main:app --reload
# Docs: http://127.0.0.1:8000/docs

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Service Counter")

# In-memory task store
_tasks: list[dict] = []


@app.get("/health")
def health():                          # <── EXPLORE: add version field
    return {"status": "ok"}


@app.get("/greet/{name}")              # <── EXPLORE: add ?lang=hi query param
def greet(name: str):
    return {"message": f"Hello, {name}!"}


class TaskIn(BaseModel):
    title: str = Field(min_length=1)


@app.post("/tasks", status_code=201)
def create_task(task: TaskIn):
    item = {"id": len(_tasks) + 1, "title": task.title, "done": False}
    _tasks.append(item)
    return item


@app.get("/tasks")
def list_tasks():
    return _tasks

# ─── CREATE ──────────────────────────────────────────────────────────────────
# Add PATCH /tasks/{task_id}/done  that marks a task as done.
# Return 404 if task_id does not exist.
