def clear_events():
    conn = _conn()
    conn.execute("DELETE FROM events")
    conn.commit()
    conn.close()
import os
import json
import sqlite3
from datetime import datetime

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data.db"))

def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            kind TEXT NOT NULL,
            request_id TEXT,
            latency_ms INTEGER,
            input_json TEXT,
            output_json TEXT
        )
        """)
        conn.commit()

def save_event(kind: str, input_data: dict, output_data: dict, latency_ms: int, request_id: str = None):
    init_db()
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as conn:
        conn.execute(
            "INSERT INTO events (ts, kind, request_id, latency_ms, input_json, output_json) VALUES (?, ?, ?, ?, ?, ?)",
            (
                ts,
                kind,
                request_id,
                int(latency_ms) if latency_ms is not None else None,
                json.dumps(input_data or {}, ensure_ascii=False),
                json.dumps(output_data or {}, ensure_ascii=False),
            ),
        )
        conn.commit()

def get_history(limit: int = 20):
    init_db()
    limit = max(1, min(int(limit), 200))

    with _conn() as conn:
        rows = conn.execute(
            "SELECT id, ts, kind, request_id, latency_ms, input_json, output_json FROM events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "ts": r["ts"],
            "kind": r["kind"],
            "request_id": r["request_id"],
            "latency_ms": r["latency_ms"],
            "input": json.loads(r["input_json"] or "{}"),
            "output": json.loads(r["output_json"] or "{}"),
        })
    return items
