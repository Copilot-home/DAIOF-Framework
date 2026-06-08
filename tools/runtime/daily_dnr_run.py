#!/usr/bin/env python3
"""Deterministic daily DNR runner template.

Design goals:
- Single execution per cycle/day via file marker guard.
- SQLite hardening with WAL and timeout.
- Safe exit semantics for launchd wrappers.
"""

from __future__ import annotations

import datetime as dt
import logging
import sqlite3
from pathlib import Path

STATE_DIR = Path.home() / ".hyperai" / "state"
LOG_DIR = Path.home() / ".hyperai" / "logs"
DB_PATH = Path.home() / "Desktop" / "workbench" / "hyperai_eternal_memories.db"
CYCLE_NAME = "daily_dnr"


def configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "daily_dnr_run.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def marker_for_today() -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    return STATE_DIR / f"{CYCLE_NAME}.{today}.done"


def already_executed_this_cycle_today() -> bool:
    return marker_for_today().exists()


def mark_cycle_complete() -> None:
    marker_for_today().write_text(dt.datetime.now(dt.timezone.utc).isoformat())


def connect_db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def run_cycle() -> None:
    if already_executed_this_cycle_today():
        logging.info("Cycle already executed today. Skipping.")
        return

    if not DB_PATH.exists():
        logging.warning("Database not found at %s. Skipping cycle.", DB_PATH)
        return

    with connect_db(DB_PATH) as conn:
        # Replace with your deterministic cycle logic.
        conn.execute(
            "CREATE TABLE IF NOT EXISTS dnr_runs (id INTEGER PRIMARY KEY, run_at TEXT NOT NULL)"
        )
        conn.execute("INSERT INTO dnr_runs(run_at) VALUES (?)", (dt.datetime.utcnow().isoformat(),))
        conn.commit()

    mark_cycle_complete()
    logging.info("Cycle complete.")


def main() -> int:
    configure_logging()
    try:
        run_cycle()
        return 0
    except sqlite3.Error:
        logging.exception("SQLite failure in daily DNR cycle")
        return 1
    except Exception:  # noqa: BLE001
        logging.exception("Unexpected failure in daily DNR cycle")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
