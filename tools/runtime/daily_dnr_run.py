#!/usr/bin/env python3
"""Deterministic daily DNR runner template.

Exit semantics:
- 0: success / skipped safely
- 1: warning (non-critical)
- 2: fail (critical)
Design goals:
- Single execution per cycle/day via file marker guard.
- SQLite hardening with WAL and timeout.
- Safe exit semantics for launchd wrappers.
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import os
import sqlite3
import subprocess
from pathlib import Path

DEFAULT_STATE_DIR = Path.home() / ".hyperai" / "state"
DEFAULT_LOG_DIR = Path.home() / ".hyperai" / "logs"
DEFAULT_DB_PATH = Path.home() / ".hyperai" / "db" / "memory.sqlite"
CYCLE_NAME = "daily_dnr"


class CycleLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.fd: int | None = None

    def __enter__(self) -> "CycleLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(self.fd, str(os.getpid()).encode())
        except FileExistsError as exc:
            raise RuntimeError(f"Lock already held: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.fd is not None:
            os.close(self.fd)
        if self.path.exists():
            self.path.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic daily DNR cycle")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--marker-dir", default=str(DEFAULT_STATE_DIR / "dnr"))
    parser.add_argument("--lock-file", default=str(DEFAULT_STATE_DIR / "dnr.lock"))
    parser.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR))
    return parser.parse_args()


def configure_logging(log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "daily_dnr_run.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def marker_for_today(marker_dir: Path) -> Path:
    marker_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    return marker_dir / f"{CYCLE_NAME}.{today}.done"

def mark_cycle_complete(marker: Path) -> None:
    tmp = marker.with_suffix(f"{marker.suffix}.tmp")
    tmp.write_text(dt.datetime.now(dt.timezone.utc).isoformat())
    tmp.replace(marker)


def wal_marker_for_db(db_path: Path, state_dir: Path) -> Path:
    db_key = db_path.resolve().as_posix().replace("/", "_")
    return state_dir / f"wal_initialized{db_key}.done"


def ensure_wal_initialized(db_path: Path, state_dir: Path) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    marker = wal_marker_for_db(db_path, state_dir)
    if marker.exists():
        return

    with sqlite3.connect(db_path, timeout=30) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")

    tmp = marker.with_suffix(f"{marker.suffix}.tmp")
    tmp.write_text(dt.datetime.now(dt.timezone.utc).isoformat())
    tmp.replace(marker)


def connect_db(db_path: Path, state_dir: Path) -> sqlite3.Connection:
    ensure_wal_initialized(db_path, state_dir)
    conn = sqlite3.connect(db_path, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def run_cycle(db_path: Path, marker_dir: Path, lock_file: Path, state_dir: Path) -> int:
    marker = marker_for_today(marker_dir)

    with CycleLock(lock_file):
        if marker.exists():
            logging.info("Cycle already executed today. Skipping.")
            return 0

        if not db_path.exists():
            logging.warning("Database not found at %s. Skipping cycle.", db_path)
            return 1

        with connect_db(db_path, state_dir) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS dnr_runs (id INTEGER PRIMARY KEY, run_at TEXT NOT NULL)"
            )
            conn.execute(
                "INSERT INTO dnr_runs(run_at) VALUES (?)",
                (dt.datetime.now(dt.timezone.utc).isoformat(),),
            )
            conn.commit()

        mark_cycle_complete(marker)
        logging.info("Cycle complete.")
        return 0




def run_preflight_gate() -> int:
    if os.environ.get("SKIP_PREFLIGHT", "0") == "1":
        return 0

    try:
        result = subprocess.run(
            ["./tools/runtime/preflight.sh", "--summary"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        return int(result.returncode)
    except Exception:
        return 1

def main() -> int:
    args = parse_args()
    db_path = Path(args.db_path).expanduser()
    marker_dir = Path(args.marker_dir).expanduser()
    lock_file = Path(args.lock_file).expanduser()
    log_dir = Path(args.log_dir).expanduser()

    state_dir = lock_file.parent
    configure_logging(log_dir)

    preflight_rc = run_preflight_gate()
    if preflight_rc == 2:
        logging.error("Preflight hard-fail. Stopping DNR cycle.")
        return 2

    try:
        return run_cycle(db_path, marker_dir, lock_file, state_dir)
    except RuntimeError:
        logging.info("Another cycle invocation is in progress. Skipping.")
        return 1
    except sqlite3.Error:
        logging.exception("SQLite failure in daily DNR cycle")
        return 2
    except Exception:  # noqa: BLE001
        logging.exception("Unexpected failure in daily DNR cycle")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
