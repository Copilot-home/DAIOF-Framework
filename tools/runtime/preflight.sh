#!/usr/bin/env bash
set -euo pipefail

MIN_FREE_GB="${MIN_FREE_GB:-15}"
STATE_DIR="${STATE_DIR:-$HOME/.hyperai/state}"
DB_PATH="${DB_PATH:-$HOME/Desktop/workbench/hyperai_eternal_memories.db}"
JOB_FILTER="${JOB_FILTER:-hyperai}"
DNR_PATH="${DNR_PATH:-$HOME/workbench/daily_dnr_run.py}"
LOG_DIR="${LOG_DIR:-$HOME/.hyperai/logs}"

status_line() {
  local label="$1"
  local state="$2"
  local detail="$3"
  printf '%s: %s (%s)\n' "$label" "$state" "$detail"
}

check_disk() {
  local free_kb free_gb
  free_kb="$(df -Pk "$HOME" | awk 'NR==2 {print $4}')"
  free_gb=$((free_kb / 1024 / 1024))

  if (( free_gb >= MIN_FREE_GB )); then
    status_line "DISK" "OK" "${free_gb}GB free (threshold ${MIN_FREE_GB}GB)"
    return 0
  fi

  status_line "DISK" "WARN" "${free_gb}GB free (threshold ${MIN_FREE_GB}GB)"
  return 1
}

check_db() {
  if [[ ! -f "$DB_PATH" ]]; then
    status_line "DB $(basename "$DB_PATH")" "WARN" "missing at $DB_PATH"
    return 1
  fi

  local tables
  if ! tables="$(sqlite3 "$DB_PATH" '.tables' 2>/dev/null)"; then
    status_line "DB $(basename "$DB_PATH")" "WARN" "cannot query tables"
    return 1
  fi

  if [[ -z "$tables" ]]; then
    status_line "DB $(basename "$DB_PATH")" "WARN" "0 tables found"
    return 1
  fi

  local table_count
  table_count="$(wc -w <<<"$tables" | tr -d ' ')"
  status_line "DB $(basename "$DB_PATH")" "OK" "${table_count} tables"
  return 0
}

check_jobs() {
  local jobs
  jobs="$(launchctl list 2>/dev/null | awk -v needle="$JOB_FILTER" '$0 ~ needle {print $3}')"

  if [[ -z "$jobs" ]]; then
    status_line "Jobs ($JOB_FILTER)" "WARN" "no loaded jobs found"
    return 1
  fi

  local count
  count="$(wc -l <<<"$jobs" | tr -d ' ')"
  status_line "Jobs ($JOB_FILTER)" "OK" "${count} loaded"
  return 0
}

check_entrypoints() {
  if [[ -f "$DNR_PATH" ]]; then
    status_line "Entrypoint daily_dnr_run.py" "OK" "$DNR_PATH"
    return 0
  fi

  status_line "Entrypoint daily_dnr_run.py" "WARN" "missing at $DNR_PATH"
  return 1
}

check_logs() {
  if [[ ! -d "$LOG_DIR" ]]; then
    status_line "Logs" "WARN" "directory missing: $LOG_DIR"
    return 1
  fi

  local oversized
  oversized="$(find "$LOG_DIR" -type f -name '*.log' -size +20M 2>/dev/null | wc -l | tr -d ' ')"

  if (( oversized == 0 )); then
    status_line "Logs" "OK" "no *.log files >20MB"
    return 0
  fi

  status_line "Logs" "WARN" "${oversized} oversized log files >20MB"
  return 1
}

main() {
  mkdir -p "$STATE_DIR"

  local score=0
  local total=5

  check_disk && ((score+=1)) || true
  check_db && ((score+=1)) || true
  check_jobs && ((score+=1)) || true
  check_entrypoints && ((score+=1)) || true
  check_logs && ((score+=1)) || true

  printf 'HEALTH_SCORE: %s/%s\n' "$score" "$total"
  if (( score < 3 )); then
    status_line "SYSTEM_STATE" "WARN" "below deterministic baseline"
    exit 1
  fi

  status_line "SYSTEM_STATE" "OK" "ready for controlled launch"
}

main "$@"
