#!/usr/bin/env python3
"""Runtime health daemon.

Periodically executes preflight and records state transitions.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import time
from pathlib import Path


STATE_NAME = {0: "OK", 1: "WARN", 2: "FAIL"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Runtime health daemon")
    parser.add_argument("--interval-seconds", type=int, default=300)
    parser.add_argument("--threshold", type=int, default=3, help="Consecutive FAIL threshold")
    parser.add_argument("--state-dir", default=str(Path.home() / ".hyperai" / "state"))
    parser.add_argument("--log-file", default=str(Path.home() / ".hyperai" / "logs" / "runtime_health_daemon.log"))
    parser.add_argument("--max-cycles", type=int, default=0, help="0 for forever")
    return parser.parse_args()


def append_log(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def run_preflight() -> int:
    if os.environ.get("SKIP_PREFLIGHT") == "1":
        return int(os.environ.get("SKIP_PREFLIGHT_RC", "0"))
    result = subprocess.run(["./tools/runtime/preflight.sh", "--summary"], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return int(result.returncode)


def main() -> int:
    args = parse_args()
    state_dir = Path(args.state_dir).expanduser()
    log_file = Path(args.log_file).expanduser()
    unhealthy_marker = state_dir / "system_unhealthy.marker"
    trend_file = state_dir / "runtime_health_trend.json"

    consecutive_failures = 0
    previous_state: str | None = None
    cycles = 0

    while True:
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        rc = run_preflight()
        state = STATE_NAME.get(rc, "FAIL")

        if rc == 2:
            consecutive_failures += 1
        else:
            consecutive_failures = 0

        event = {
            "timestamp": now,
            "exit_code": rc,
            "state": state,
            "consecutive_failures": consecutive_failures,
        }

        state_changed = previous_state != state
        if state_changed:
            event["event"] = "state_changed"
        append_log(log_file, event)

        trend_file.parent.mkdir(parents=True, exist_ok=True)
        trend_file.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding="utf-8")

        if consecutive_failures >= args.threshold:
            unhealthy_marker.write_text(now, encoding="utf-8")
        elif unhealthy_marker.exists():
            unhealthy_marker.unlink()

        previous_state = state
        cycles += 1
        if args.max_cycles and cycles >= args.max_cycles:
            break
        time.sleep(args.interval_seconds)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
