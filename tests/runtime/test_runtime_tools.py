import os
import sys
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "tools/runtime/preflight.sh"
DNR = ROOT / "tools/runtime/daily_dnr_run.py"
DAEMON = ROOT / "tools/runtime/runtime_health_daemon.py"


class RuntimeToolsTests(unittest.TestCase):
    def test_preflight_fail_on_invalid_disk_path(self):
        if sys.platform == "win32":
            self.skipTest("preflight.sh is a POSIX shell runtime check")
        env = os.environ.copy()
        env["DISK_PATH"] = "/path/does/not/exist"
        result = subprocess.run([str(PREFLIGHT), "--summary"], cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)

    def test_daily_dnr_idempotent_same_day(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            db = td_path / "memory.sqlite"
            log_dir = td_path / "logs"
            marker_dir = td_path / "state/dnr"
            lock_file = td_path / "state/dnr.lock"
            db.parent.mkdir(parents=True, exist_ok=True)
            sqlite3.connect(db).close()

            env = os.environ.copy()
            env["SKIP_PREFLIGHT"] = "1"

            cmd = [
                sys.executable,
                str(DNR),
                "--db-path",
                str(db),
                "--marker-dir",
                str(marker_dir),
                "--lock-file",
                str(lock_file),
                "--log-dir",
                str(log_dir),
            ]
            first = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
            second = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)

            self.assertEqual(first.returncode, 0)
            self.assertEqual(second.returncode, 0)

    def test_health_daemon_writes_trend(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            state_dir = td_path / "state"
            log_file = td_path / "logs/daemon.log"
            env = os.environ.copy()
            env["DISK_PATH"] = "/path/does/not/exist"
            env["SKIP_PREFLIGHT"] = "1"
            env["SKIP_PREFLIGHT_RC"] = "2"

            cmd = [
                sys.executable,
                str(DAEMON),
                "--interval-seconds",
                "1",
                "--threshold",
                "1",
                "--state-dir",
                str(state_dir),
                "--log-file",
                str(log_file),
                "--max-cycles",
                "1",
            ]
            result = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertTrue((state_dir / "runtime_health_trend.json").exists())
            self.assertTrue((state_dir / "system_unhealthy.marker").exists())


if __name__ == "__main__":
    unittest.main()
