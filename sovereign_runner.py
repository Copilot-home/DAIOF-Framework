#!/usr/bin/env python3
"""
Sovereign Runner Daemon 🏭🚀☠️
Local Orchestrator for HyperAI Autonomous Brains

Developed by Antigravity for alpha_prime_omega
Bypasses GitHub Actions Quota limitations via direct local execution.

⚠️  LOCAL-ONLY TOOL — NOT FOR CI/CD OR PRODUCTION USE.
    This daemon is designed to run on the developer's macOS workstation
    (hard-coded paths under /Users/andy/). It orchestrates the same scripts
    that .github/workflows/ runs, but locally, to avoid GitHub Actions
    quota consumption during development.

    Do NOT deploy this in Docker, Kubernetes, or any shared server.
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Setup Paths
BASE_DIR = Path("/Users/andy/my_too_test")
FRAMEWORK_DIR = BASE_DIR / "DAIOF-Framework"
SCRIPTS_DIR = FRAMEWORK_DIR / ".github" / "scripts"
LOG_DIR = FRAMEWORK_DIR / "logs" / "sovereign_runner"
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python3"

# Ensure directories exist
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "sovereign.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SOVEREIGN_RUNNER")

class SovereignRunner:
    def __init__(self):
        self.is_running = False
        self.brains = [
            {
                "name": "RealtimeTaskGenerator",
                "path": SCRIPTS_DIR / "realtime_task_generator.py",
                "interval": 30, # seconds
                "last_run": 0
            },
            {
                "name": "HealthMonitor",
                "path": SCRIPTS_DIR / "health_monitor.py",
                "interval": 300, # 5 minutes
                "last_run": 0
            },
            {
                "name": "MetricsDashboard",
                "path": SCRIPTS_DIR / "metrics_dashboard.py",
                "interval": 600, # 10 minutes
                "last_run": 0
            }
        ]
        logger.info("⚡ Sovereign Runner initialized. Quota restrictions neutralized.")

    def execute_brain(self, brain):
        name = brain["name"]
        path = brain["path"]
        logger.info(f"⚔️ Engaging Brain: {name}")
        
        try:
            # We run in a separate process to avoid blocking the orchestrator
            # Using the Master's .venv to ensure dependencies are met
            result = subprocess.run(
                [str(VENV_PYTHON), str(path)],
                cwd=str(FRAMEWORK_DIR),
                capture_output=True,
                text=True,
                timeout=120 # Prevent infinite hangs
            )
            
            if result.returncode == 0:
                logger.info(f"✅ {name} execution successful.")
                # Log outcome to a specific brain log file
                with open(LOG_DIR / f"{name}_pulse.log", "a") as f:
                    f.write(f"[{datetime.now()}] SUCCESS\n{result.stdout}\n")
            else:
                logger.error(f"❌ {name} failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"🚨 Critical Failure in {name}: {e}")

    def run(self):
        self.is_running = True
        logger.info("🚀 Sovereign Runner: ACTIVE PATROL STARTING")
        
        try:
            while self.is_running:
                now = time.time()
                for brain in self.brains:
                    if now - brain["last_run"] >= brain["interval"]:
                        self.execute_brain(brain)
                        brain["last_run"] = now
                
                time.sleep(1) # Frequency modulation
        except KeyboardInterrupt:
            logger.info("⏹️ Sovereign Runner: HALTING BY MASTER COMMAND")
            self.is_running = False

if __name__ == "__main__":
    runner = SovereignRunner()
    runner.run()
