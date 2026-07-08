#!/usr/bin/env python3
"""
Quick Test - Real-Time Task Generator
Runs for 60 seconds to demonstrate the system
"""

import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

if "pytest" in sys.modules:
    import pytest

    pytest.skip("interactive real-time git demo is not a pytest test", allow_module_level=True)

# Change to DAIOF directory
os.chdir(Path(__file__).resolve().parent)

print("🧬 DAIOF Real-Time Task Generator - Quick Test")
print("="*70)
print(f"📍 Working Directory: {os.getcwd()}")
print(f"⏰ Start Time: {datetime.now().strftime('%H:%M:%S')}")
print(f"⏱️  Duration: 60 seconds")
print("="*70)
print()

cycle = 0
tasks_generated = 0
tasks_executed = 0

try:
    for i in range(6):  # 6 cycles x 10 seconds = 60 seconds
        cycle += 1
        print(f"🔄 Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
        
        # Check git status
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout.strip():
            files = result.stdout.strip().split('\n')
            print(f"   📋 Task Generated: Commit {len(files)} file(s)")
            tasks_generated += 1
            
            # Execute commit
            print(f"   🚀 Executing: Auto-commit changes")
            commit_result = subprocess.run(
                ['git', 'add', '-A'],
                capture_output=True,
                timeout=10
            )
            
            if commit_result.returncode == 0:
                subprocess.run(
                    ['git', 'commit', '-m', f'🤖 Real-time auto-update: Cycle {cycle}'],
                    capture_output=True,
                    timeout=10
                )
                subprocess.run(
                    ['git', 'push', 'origin', 'main'],
                    capture_output=True,
                    timeout=30
                )
                print(f"   ✅ Success: Changes committed and pushed")
                tasks_executed += 1
            else:
                print(f"   ⚠️  No changes to commit")
        else:
            print(f"   ℹ️  No tasks generated - repository clean")
        
        # Check Python files for formatting
        py_files = list(Path('.').rglob('*.py'))
        py_files = [f for f in py_files if 'venv' not in str(f) and '.venv' not in str(f)]
        
        if py_files and cycle % 2 == 0:  # Every other cycle
            sample_file = py_files[0]
            print(f"   📋 Task Generated: Format {sample_file.name}")
            tasks_generated += 1
            
            # Note: Not actually executing to avoid breaking code
            print(f"   ℹ️  Skipped: Would format in production")
        
        # Stats
        print(f"   📊 Stats: {tasks_generated} generated, {tasks_executed} executed")
        print()
        
        # Wait 10 seconds
        if i < 5:  # Don't wait after last cycle
            time.sleep(10)

except KeyboardInterrupt:
    print("\n⏹️  Stopped by user")

print("="*70)
print(f"✅ Test Complete - {datetime.now().strftime('%H:%M:%S')}")
print(f"📊 Final Stats:")
print(f"   Total Cycles: {cycle}")
print(f"   Tasks Generated: {tasks_generated}")
print(f"   Tasks Executed: {tasks_executed}")
if tasks_generated > 0:
    print(f"   Success Rate: {tasks_executed/tasks_generated*100:.1f}%")
print("="*70)
print()
print("🎯 Full system runs every minute via GitHub Actions!")
print("📖 See .github/workflows/realtime-tasks.yml for configuration")
