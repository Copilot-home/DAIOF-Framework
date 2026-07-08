#!/usr/bin/env python3
"""Local CI/CD operator for DAIOF.

The operator makes local automation explicit and evidence-driven:

- dry-run by default;
- verification before commit or merge;
- no force/reset/destructive git operations;
- optional push only via --push;
- proof artifacts for every run under .runtime/local-cicd/.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_DIR = ROOT / ".runtime" / "local-cicd"
DEFAULT_REMOTE = "origin"
DEFAULT_MAIN = "main"


def executable(name: str) -> str:
    if os.name == "nt" and not name.endswith(".cmd"):
        cmd = shutil.which(f"{name}.cmd")
        if cmd:
            return cmd
    return shutil.which(name) or name


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(
    args: list[str],
    *,
    timeout: int = 120,
    check: bool = False,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    completed = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
        env={**os.environ, **(env or {})},
    )
    result = {
        "cmd": args,
        "returncode": completed.returncode,
        "ok": completed.returncode == 0,
        "duration_seconds": round(time.monotonic() - started, 3),
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }
    if check and completed.returncode != 0:
        raise RuntimeError(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def git(args: list[str], **kwargs: Any) -> dict[str, Any]:
    return run([executable("git"), *args], **kwargs)


def write_proof(payload: dict[str, Any]) -> Path:
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = PROOF_DIR / f"{payload['operation']}_{stamp}.json"
    latest = PROOF_DIR / f"{payload['operation']}_latest.json"
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    return path


def status_snapshot() -> dict[str, Any]:
    return {
        "branch": git(["branch", "--show-current"]),
        "status": git(["status", "--short", "--branch"]),
        "porcelain": git(["status", "--porcelain=v1"]),
        "remote": git(["remote", "-v"]),
        "upstream": git(
            ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]
        ),
        "ahead_behind": git(["rev-list", "--left-right", "--count", "HEAD...@{u}"]),
        "worktrees": git(["worktree", "list", "--porcelain"]),
    }


def changed_paths() -> list[str]:
    result = git(["status", "--porcelain=v1"])
    if not result["ok"] or not result["stdout"]:
        return []
    paths: list[str] = []
    for line in result["stdout"].splitlines():
        if not line.strip():
            continue
        path = line[2:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return paths


def is_forbidden_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    forbidden_prefixes = (
        ".env",
        ".venv/",
        "node_modules/",
        ".runtime/",
        "logs/",
        "metrics/",
        ".git/",
    )
    return normalized.startswith(forbidden_prefixes) or normalized.endswith(".log")


def run_runtime_smoke() -> dict[str, Any]:
    import socket

    try:
        with socket.create_connection(("127.0.0.1", 5000), timeout=0.25):
            port_free = False
    except OSError:
        port_free = True

    if not port_free:
        return {
            "ok": True,
            "skipped": True,
            "reason": "port 5000 already in use; node test suite covers dynamic server smoke",
        }

    process = subprocess.Popen(
        [executable("node"), "apps/sse-gateway/server.mjs"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "PORT": "5000"},
    )
    try:
        deadline = time.time() + 8
        last_error: str | None = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen("http://127.0.0.1:5000/", timeout=1) as res:
                    body = res.read().decode("utf-8")
                    return {"ok": res.status == 200, "status": res.status, "body": body}
            except (OSError, urllib.error.URLError) as exc:
                last_error = str(exc)
                time.sleep(0.2)
        return {"ok": False, "error": last_error or "server did not become ready"}
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def verify() -> dict[str, Any]:
    checks = [
        run([executable("node"), "--check", "apps/sse-gateway/server.mjs"]),
        run([executable("npm"), "test"], timeout=180),
        run([executable("python"), "-m", "py_compile", "digital_ai_organism_framework.py"]),
        run([executable("python"), "-m", "py_compile", "haios_core.py"]),
        run([executable("python"), "-m", "py_compile", "haios_runtime.py"]),
        run([executable("python"), "tools/governance/governance_gate.py", "validate"], timeout=180),
    ]
    smoke = run_runtime_smoke()
    ok = all(item["ok"] for item in checks) and smoke["ok"]
    return {"ok": ok, "checks": checks, "runtime_smoke": smoke}


def ensure_clean_index() -> None:
    diff_index = git(["diff", "--cached", "--name-only"])
    if diff_index["ok"] and diff_index["stdout"]:
        raise RuntimeError("staged changes already exist; refusing to overwrite index")


def autocommit(args: argparse.Namespace, proof: dict[str, Any]) -> None:
    verify_result = verify()
    proof["verification"] = verify_result
    if not verify_result["ok"]:
        proof["decision"] = "blocked"
        proof["reason"] = "verification failed"
        return

    paths = changed_paths()
    proof["candidate_paths"] = paths
    forbidden = [path for path in paths if is_forbidden_path(path)]
    if forbidden:
        proof["decision"] = "blocked"
        proof["reason"] = "forbidden runtime/secret/generated paths present"
        proof["forbidden_paths"] = forbidden
        return
    if not paths:
        proof["decision"] = "noop"
        proof["reason"] = "no changes to commit"
        return
    if not args.execute:
        proof["decision"] = "dry_run"
        proof["reason"] = "would stage candidate paths and commit after --execute"
        return

    ensure_clean_index()
    git(["add", "--", *paths], check=True)
    commit = git(["commit", "-m", args.message], check=False)
    proof["commit"] = commit
    if not commit["ok"]:
        proof["decision"] = "blocked"
        proof["reason"] = "git commit failed"
        return
    proof["decision"] = "committed"

    if args.push:
        push = git(["push", "-u", args.remote, git(["branch", "--show-current"])["stdout"]])
        proof["push"] = push
        if not push["ok"]:
            proof["decision"] = "blocked"
            proof["reason"] = "commit succeeded but push failed"


def automerge(args: argparse.Namespace, proof: dict[str, Any]) -> None:
    branch = git(["branch", "--show-current"])["stdout"]
    proof["source_branch"] = branch
    if branch == args.main_branch:
        proof["decision"] = "noop"
        proof["reason"] = "already on main branch"
        return
    if changed_paths():
        proof["decision"] = "blocked"
        proof["reason"] = "working tree must be clean before automerge"
        return

    verify_result = verify()
    proof["verification"] = verify_result
    if not verify_result["ok"]:
        proof["decision"] = "blocked"
        proof["reason"] = "verification failed"
        return
    if not args.execute:
        proof["decision"] = "dry_run"
        proof["reason"] = f"would merge {branch} into {args.main_branch} after --execute"
        return

    git(["checkout", args.main_branch], check=True)
    git(["pull", "--ff-only", args.remote, args.main_branch], check=True)
    merge = git(["merge", "--no-ff", branch, "-m", f"Merge {branch} into {args.main_branch}"])
    proof["merge"] = merge
    if not merge["ok"]:
        proof["decision"] = "blocked"
        proof["reason"] = "merge failed; manual conflict resolution required"
        return
    proof["decision"] = "merged"
    if args.push:
        push = git(["push", args.remote, args.main_branch])
        proof["push"] = push
        if not push["ok"]:
            proof["decision"] = "blocked"
            proof["reason"] = "merge succeeded locally but push failed"


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="operation", required=True)

    sub.add_parser("status")
    sub.add_parser("verify")

    commit_parser = sub.add_parser("autocommit")
    commit_parser.add_argument("--message", default="chore: local DAIOF automation update")
    commit_parser.add_argument("--execute", action="store_true")
    commit_parser.add_argument("--push", action="store_true")
    commit_parser.add_argument("--remote", default=DEFAULT_REMOTE)

    merge_parser = sub.add_parser("automerge")
    merge_parser.add_argument("--main-branch", default=DEFAULT_MAIN)
    merge_parser.add_argument("--execute", action="store_true")
    merge_parser.add_argument("--push", action="store_true")
    merge_parser.add_argument("--remote", default=DEFAULT_REMOTE)

    args = parser.parse_args()
    proof: dict[str, Any] = {
        "operation": args.operation,
        "created_at": utc_now(),
        "repo": str(ROOT),
        "execute": bool(getattr(args, "execute", False)),
        "push": bool(getattr(args, "push", False)),
        "status_before": status_snapshot(),
    }

    try:
        if args.operation == "status":
            proof["decision"] = "observed"
        elif args.operation == "verify":
            proof["verification"] = verify()
            proof["decision"] = "verified" if proof["verification"]["ok"] else "failed"
        elif args.operation == "autocommit":
            autocommit(args, proof)
        elif args.operation == "automerge":
            automerge(args, proof)
        else:
            raise RuntimeError(f"unknown operation: {args.operation}")
    except Exception as exc:  # noqa: BLE001 - operator must produce proof.
        proof["decision"] = "error"
        proof["error"] = str(exc)

    proof["status_after"] = status_snapshot()
    path = write_proof(proof)
    print(json.dumps({"decision": proof["decision"], "proof": str(path)}, ensure_ascii=False))
    return 0 if proof["decision"] in {"observed", "verified", "noop", "dry_run", "committed", "merged"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
