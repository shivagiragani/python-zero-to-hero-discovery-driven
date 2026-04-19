// ─── Sandbox: The Delivery Route (REST Integration) ─────────────────────────
// Analogy: Order slip moves from front desk (React) → kitchen (FastAPI) → back.
// The fetch call is the slip; the response display is the receipt.

import { useState } from "react";

const API = "http://localhost:8000";   // <── EXPLORE: read from env var

export default function App() {
  const [tasks, setTasks]       = useState([]);
  const [title, setTitle]       = useState("");
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState("");

  async function fetchTasks() {
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`${API}/tasks`);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setTasks(await r.json());
    } catch (e) {
      setError(e.message);            // <── EXPLORE: add retry button
    } finally {
      setLoading(false);
    }
  }

  async function addTask(e) {
    e.preventDefault();
    if (!title.trim()) return;
    await fetch(`${API}/tasks`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ title }),
    });
    setTitle("");
    fetchTasks();                     // refresh list
  }

  // CREATE: show a "done" badge for completed tasks
  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem", maxWidth: "480px" }}>
      <h1>Task Delivery Route</h1>
      <form onSubmit={addTask} style={{ display: "flex", gap: "0.5rem" }}>
        <input value={title} onChange={e => setTitle(e.target.value)}
               placeholder="New task" style={{ flex: 1 }} />
        <button type="submit">Add</button>
      </form>
      <button onClick={fetchTasks} style={{ marginTop: "1rem" }}>Refresh</button>
      {loading && <p>Loading…</p>}
      {error   && <p style={{ color: "crimson" }}>Error: {error}</p>}
      <ul>{tasks.map(t => <li key={t.id}>{t.title}</li>)}</ul>
    </div>
  );
}
