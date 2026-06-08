# Runtime Stability Blueprint (Deterministic Execution)

This blueprint encodes a strict stabilization order for local runtime reliability:

1. Disk stabilization (>= 15GB free)
2. Daily cycle de-duplication
3. Launch wrapper normalization
4. SQLite lock hardening (WAL + timeout)
5. Deterministic log rotation
6. Preflight gate before enabling all jobs

## Runtime State Table

| Job | Schedule | Entry Script | Writes DB | Writes Logs | Risk |
| --- | --- | --- | --- | --- | --- |
| `com.hyperai.os.master` | `StartInterval=300`, `KeepAlive=true` | `launchd_safe_wrapper.sh` -> `daily_dnr_run.py` | Yes | Yes | Respawn amplification if non-zero exits are unbounded. |
| `com.hyperai.daily_dnr` | Daily | `daily_dnr_run.py` | Yes | Yes | Multi-run inflation without cycle marker guard. |
| `com.hyperai.preflight` | Manual / pre-enable gate | `preflight.sh` | Read-only check | Yes (stdout/stderr) | False confidence if checks are skipped. |
| `com.hyperai.logrotate` | Hourly / daily | `rotate_hyperai_logs.sh` | No | Yes | Disk pressure if rotation is absent or retention is too long. |

## Critical Gates

- **Disk floor**: Keep at least **15GB free** before enabling autonomous jobs.
- **Launch safety**: Wrapper scripts should emit diagnostics and end with `exit 0` unless a hard stop is required.
- **DB lock mitigation**: Use `sqlite3.connect(timeout=30)` and `PRAGMA journal_mode=WAL`.
- **Daily cycle guard**: Enforce one run per day/cycle with marker files in `~/.hyperai/state/`.

## Low-Risk Cleanup Commands

```bash
rm -rf ~/Library/Caches/ms-playwright*
rm -rf ~/Library/Caches/pip
brew cleanup -s
```

Do **not** remove canonical model storage (`~/.aitk/models`) without explicit migration planning.

## Suggested Launch Sequence

1. Run `tools/runtime/preflight.sh`
2. Load jobs one-by-one
3. Observe logs for 10-15 minutes
4. Only then enable full KeepAlive set
