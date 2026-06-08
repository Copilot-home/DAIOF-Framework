#!/usr/bin/env bash
set -euo pipefail

ORIG="${ORIG:-$HOME/workbench/daily_dnr_run.py}"
ERR_LOG="${ERR_LOG:-$HOME/.hyperai/logs/os_master.error.log}"
RUN_LOG="${RUN_LOG:-$HOME/.hyperai/logs/os_master.log}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

mkdir -p "$(dirname "$ERR_LOG")"

ts() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

if [[ ! -f "$ORIG" ]]; then
  echo "$(ts) Missing entrypoint: $ORIG" >> "$ERR_LOG"
  exit 0
fi

if ! "$PYTHON_BIN" "$ORIG" >> "$RUN_LOG" 2>> "$ERR_LOG"; then
  echo "$(ts) Entrypoint failed: $ORIG" >> "$ERR_LOG"
fi

exit 0
