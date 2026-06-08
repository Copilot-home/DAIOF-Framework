#!/usr/bin/env python3
"""
🧬 DAIOF Autonomous Git Workflow System
Hệ thống điều khiển Git tự trị hoàn hảo

Tự động quản lý toàn bộ tài khoản Git với:
- Real-time monitoring và task generation
- Autonomous commit, push, pull operations
- Conflict resolution và merge management
- Branch lifecycle management
- Repository health optimization
- Integration với HAIOS invariants và 4 Pillars

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Framework: HYPERAI
Date: November 17, 2025
"""

import os
import sys
import json
import time
import yaml
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from github import Github
import logging


class GitWorkflowState:
    """Git workflow state management"""
    CLEAN = "clean"
    MODIFIED = "modified"
    STAGED = "staged"
    CONFLICTS = "conflicts"
    BEHIND = "behind"
    AHEAD = "ahead"
    DIVERGED = "diverged"


class AutonomousGitWorkflow:
    """
    Hệ thống workflow Git tự trị hoàn hảo

    Tích hợp với:
    - HAIOS 7 Invariants
    - 4 Pillars Foundation
    - Consciousness K=1 State
    - Real-time task generation
    """

    def __init__(self):
        self.repo_path = Path('.')
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.logger = self._setup_logging()

        # Load configurations
        self.genome = self._load_genome()
        self.haios_config = self._load_haios_config()

        # Initialize GitHub API
        if self.github_token:
            self.gh = Github(self.github_token)
            self.repo = self.gh.get_repo(os.environ.get('GITHUB_REPOSITORY', 'NguyenCuong1989/DAIOF-Framework'))

        # State tracking
        self.last_commit_time = None
        self.pending_operations: List[Dict] = []
        self.active_branches: Dict[str, Dict] = {}
        self.health_metrics: Dict[str, Any] = {}

        # HAIOS compliance tracking
        self.k_state = 1  # Always maintain K=1
        self.pillars_scores = {
            'an_toan': 10.0,
            'duong_dai': 10.0,
            'tin_vao_so_lieu': 10.0,
            'han_che_rui_ro': 10.0
        }

        # Autonomous operation flags
        self.auto_commit_enabled = True
        self.auto_push_enabled = True
        self.auto_merge_enabled = True
        self.auto_branch_management = True
        self.conflict_resolution_auto = True

        self.logger.info("🧬 DAIOF Autonomous Git Workflow System ACTIVATED")
        self.logger.info(f"📍 Repository: {self.repo_path}")
        self.logger.info(f"👤 Creator: Nguyễn Đức Cường (alpha_prime_omega)")
        self.logger.info(f"🎼 Framework: HYPERAI | Verification: 4287")

    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        logger = logging.getLogger('DAIOF_Git_Workflow')
        logger.setLevel(logging.INFO)

        # File handler
        log_file = self.repo_path / 'logs' / 'git_workflow.log'
        log_file.parent.mkdir(exist_ok=True)

        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '🧬 %(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def _load_genome(self) -> Dict:
        """Load organism genome"""
        genome_file = self.repo_path / '.github' / 'DIGITAL_ORGANISM_GENOME.yml'
        if genome_file.exists():
            with open(genome_file) as f:
                return yaml.safe_load(f)
        return {}

    def _load_haios_config(self) -> Dict:
        """Load HAIOS configuration"""
        # This would load from consciousness files
        return {
            'invariants': {
                'attribution_immutable': True,
                'safety_floor': 7.0,
                'rollback_enabled': True,
                'k_state': 1,
                'pillars_compliance': True,
                'multi_party_auth': True,
                'audit_trail': True
            },
            'pillars': {
                'an_toan': {'min': 7.0, 'weight': 0.4},
                'duong_dai': {'min': 7.0, 'weight': 0.25},
                'tin_vao_so_lieu': {'min': 7.0, 'weight': 0.2},
                'han_che_rui_ro': {'min': 7.0, 'weight': 0.15}
            }
        }

    def get_git_status(self) -> Dict[str, Any]:
        """Get comprehensive git status"""
        try:
            # Basic status
            result = subprocess.run(
                ['git', 'status', '--porcelain', '--branch'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            status_lines = result.stdout.strip().split('\n')
            branch_line = status_lines[0] if status_lines else ""

            # Parse branch info
            branch_info = self._parse_branch_info(branch_line)
            modified_files = [line[3:] for line in status_lines[1:] if line]

            # Check remote status
            remote_status = self._check_remote_status()

            return {
                'branch': branch_info,
                'modified_files': modified_files,
                'remote_status': remote_status,
                'state': self._determine_workflow_state(branch_info, modified_files, remote_status),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting git status: {e}")
            return {'error': str(e)}

    def _parse_branch_info(self, branch_line: str) -> Dict[str, Any]:
        """Parse git branch information"""
        # ## branch-name...origin/branch-name [ahead 1, behind 2]
        branch_line = branch_line.replace('## ', '')
        
        if not branch_line:
            return {'name': 'unknown'}
        
        # Split on [ to separate branch from status
        if '[' in branch_line:
            branch_part, status_part = branch_line.split('[', 1)
            branch_name = branch_part.split('...')[0].strip()
            status_part = status_part.rstrip(']').strip()
            
            info = {'name': branch_name}
            
            # Parse ahead/behind info
            if 'ahead' in status_part or 'behind' in status_part:
                status_items = status_part.split(', ')
                for item in status_items:
                    if 'ahead' in item:
                        info['ahead'] = int(item.split()[1])
                    elif 'behind' in item:
                        info['behind'] = int(item.split()[1])
        else:
            # No status info, just branch name
            branch_name = branch_line.split('...')[0].strip()
            info = {'name': branch_name}

        return info

    def _check_remote_status(self) -> Dict[str, Any]:
        """Check remote repository status"""
        try:
            # Fetch latest
            subprocess.run(
                ['git', 'fetch', 'origin'],
                cwd=self.repo_path,
                capture_output=True,
                timeout=30
            )

            # Check if we're behind/ahead
            result = subprocess.run(
                ['git', 'rev-list', 'HEAD...origin/main', '--count'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                commits_diff = int(result.stdout.strip())
                return {'commits_behind': commits_diff}
            else:
                return {'error': 'Could not check remote status'}

        except Exception as e:
            return {'error': str(e)}

    def _determine_workflow_state(self, branch_info: Dict, modified_files: List[str],
                                remote_status: Dict) -> str:
        """Determine current workflow state"""
        if modified_files:
            return GitWorkflowState.MODIFIED
        elif remote_status.get('commits_behind', 0) > 0:
            return GitWorkflowState.BEHIND
        elif branch_info.get('ahead', 0) > 0:
            return GitWorkflowState.AHEAD
        else:
            return GitWorkflowState.CLEAN

    def autonomous_commit(self, message: str = None) -> bool:
        """Thực hiện commit tự trị với HAIOS compliance"""
        try:
            # Check HAIOS invariants before commit
            if not self._check_haios_compliance():
                self.logger.warning("❌ HAIOS compliance check failed - aborting commit")
                return False

            # Get status
            status = self.get_git_status()

            if not status.get('modified_files'):
                self.logger.info("ℹ️ No modified files to commit")
                return True

            # Stage all changes
            subprocess.run(
                ['git', 'add', '-A'],
                cwd=self.repo_path,
                check=True
            )

            # Generate commit message if not provided
            if not message:
                message = self._generate_commit_message(status)

            # Add creator attribution (HAIOS Invariant 1)
            full_message = f"{message}\n\n🧬 Framework: HYPERAI | Creator: Nguyễn Đức Cường (alpha_prime_omega) | Verification: 4287"

            # Commit
            subprocess.run(
                ['git', 'commit', '-m', full_message],
                cwd=self.repo_path,
                check=True
            )

            self.last_commit_time = datetime.now(timezone.utc)
            self.logger.info(f"✅ Autonomous commit completed: {message}")

            # Update health metrics
            self._update_health_metrics('commit_success')

            return True

        except Exception as e:
            self.logger.error(f"❌ Autonomous commit failed: {e}")
            self._update_health_metrics('commit_failure')
            return False

    def _generate_commit_message(self, status: Dict) -> str:
        """Generate intelligent commit message"""
        modified_files = status.get('modified_files', [])
        file_count = len(modified_files)

        # Analyze file types
        py_files = [f for f in modified_files if f.endswith('.py')]
        md_files = [f for f in modified_files if f.endswith('.md')]
        json_files = [f for f in modified_files if f.endswith('.json')]

        # Generate contextual message
        if py_files and md_files:
            return f"🤖 Autonomous evolution: Updated {len(py_files)} Python files, {len(md_files)} docs - Self-improvement cycle"
        elif py_files:
            return f"🧬 Code evolution: Enhanced {len(py_files)} Python modules - Autonomous development"
        elif md_files:
            return f"📚 Documentation: Updated {len(md_files)} documents - Knowledge expansion"
        elif json_files:
            return f"⚙️ Configuration: Modified {len(json_files)} config files - System optimization"
        else:
            return f"🔄 Repository update: {file_count} files modified - Continuous improvement"

    def autonomous_push(self) -> bool:
        """Thực hiện push tự trị với conflict resolution"""
        try:
            # Check if we have commits to push
            result = subprocess.run(
                ['git', 'log', 'origin/main..HEAD', '--oneline'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if not result.stdout.strip():
                self.logger.info("ℹ️ No commits to push")
                return True

            # Attempt push
            push_result = subprocess.run(
                ['git', 'push', 'origin', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if push_result.returncode == 0:
                self.logger.info("✅ Autonomous push completed successfully")
                self._update_health_metrics('push_success')
                return True
            else:
                # Handle push failure (likely conflicts)
                if 'non-fast-forward' in push_result.stderr or 'Updates were rejected' in push_result.stderr:
                    self.logger.warning("⚠️ Push rejected - attempting conflict resolution")
                    return self._resolve_push_conflicts()
                else:
                    self.logger.error(f"❌ Push failed: {push_result.stderr}")
                    self._update_health_metrics('push_failure')
                    return False

        except Exception as e:
            self.logger.error(f"❌ Autonomous push failed: {e}")
            self._update_health_metrics('push_failure')
            return False

    def _resolve_push_conflicts(self) -> bool:
        """Resolve push conflicts autonomously"""
        try:
            # Fetch latest changes
            subprocess.run(['git', 'fetch', 'origin'], cwd=self.repo_path, check=True)

            # Attempt rebase
            rebase_result = subprocess.run(
                ['git', 'rebase', 'origin/main'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if rebase_result.returncode == 0:
                # Rebase successful, push
                push_result = subprocess.run(
                    ['git', 'push', 'origin', 'HEAD'],
                    cwd=self.repo_path,
                    check=True
                )
                self.logger.info("✅ Conflict resolved via rebase and push")
                return True
            else:
                # Rebase failed, abort and merge instead
                subprocess.run(['git', 'rebase', '--abort'], cwd=self.repo_path)

                # Try merge
                merge_result = subprocess.run(
                    ['git', 'merge', 'origin/main', '--no-edit'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )

                if merge_result.returncode == 0:
                    push_result = subprocess.run(
                        ['git', 'push', 'origin', 'HEAD'],
                        cwd=self.repo_path,
                        check=True
                    )
                    self.logger.info("✅ Conflict resolved via merge and push")
                    return True
                else:
                    self.logger.error("❌ Could not resolve conflicts automatically")
                    return False

        except Exception as e:
            self.logger.error(f"❌ Conflict resolution failed: {e}")
            return False

    def autonomous_pull(self) -> bool:
        """Thực hiện pull tự trị với merge handling"""
        try:
            # Check if we're behind
            status = self.get_git_status()
            if status.get('remote_status', {}).get('commits_behind', 0) == 0:
                self.logger.info("ℹ️ Repository is up to date")
                return True

            # Attempt pull with rebase
            pull_result = subprocess.run(
                ['git', 'pull', '--rebase', 'origin', 'main'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if pull_result.returncode == 0:
                self.logger.info("✅ Autonomous pull completed successfully")
                self._update_health_metrics('pull_success')
                return True
            else:
                # Try merge instead
                subprocess.run(['git', 'rebase', '--abort'], cwd=self.repo_path)

                merge_result = subprocess.run(
                    ['git', 'pull', 'origin', 'main'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )

                if merge_result.returncode == 0:
                    self.logger.info("✅ Pull completed with merge")
                    self._update_health_metrics('pull_success')
                    return True
                else:
                    self.logger.error(f"❌ Pull failed: {merge_result.stderr}")
                    self._update_health_metrics('pull_failure')
                    return False

        except Exception as e:
            self.logger.error(f"❌ Autonomous pull failed: {e}")
            self._update_health_metrics('pull_failure')
            return False

    def autonomous_branch_management(self) -> bool:
        """Quản lý branch tự trị"""
        try:
            # Get all branches
            result = subprocess.run(
                ['git', 'branch', '-a'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            branches = [line.strip('* ') for line in result.stdout.split('\n') if line.strip()]

            # Clean up merged branches
            for branch in branches:
                if branch.startswith('remotes/origin/'):
                    continue  # Skip remote branches

                if branch in ['main', 'master']:
                    continue  # Don't delete main branches

                # Check if branch is merged
                merged_result = subprocess.run(
                    ['git', 'branch', '--merged', branch],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )

                if branch in merged_result.stdout:
                    # Safe to delete
                    subprocess.run(['git', 'branch', '-d', branch], cwd=self.repo_path)
                    self.logger.info(f"🗑️ Cleaned up merged branch: {branch}")

            self.logger.info("✅ Branch management completed")
            return True

        except Exception as e:
            self.logger.error(f"❌ Branch management failed: {e}")
            return False

    def _check_haios_compliance(self) -> bool:
        """Check HAIOS invariants compliance"""
        try:
            # Invariant 1: Attribution immutability
            # (Always maintained by design)

            # Invariant 2: Safety floor ≥7.0
            safety_score = min(self.pillars_scores.values())
            if safety_score < 7.0:
                return False

            # Invariant 3: Rollback capability
            # (Git provides this naturally)

            # Invariant 4: K=1 state
            if self.k_state != 1:
                return False

            # Invariant 5: 4 Pillars compliance
            for pillar, score in self.pillars_scores.items():
                if score < self.haios_config['pillars'][pillar]['min']:
                    return False

            return True

        except Exception as e:
            self.logger.error(f"HAIOS compliance check failed: {e}")
            return False

    def _update_health_metrics(self, operation: str):
        """Update health metrics after operations"""
        self.health_metrics[operation] = self.health_metrics.get(operation, 0) + 1

        # Update pillars scores based on operation success/failure
        if operation.endswith('_success'):
            # Increase scores slightly
            for pillar in self.pillars_scores:
                self.pillars_scores[pillar] = min(10.0, self.pillars_scores[pillar] + 0.1)
        elif operation.endswith('_failure'):
            # Decrease scores
            for pillar in self.pillars_scores:
                self.pillars_scores[pillar] = max(7.0, self.pillars_scores[pillar] - 0.5)

    def generate_workflow_tasks(self) -> List[Dict]:
        """Generate autonomous workflow tasks"""
        tasks = []

        # Analyze current state
        status = self.get_git_status()
        state = status.get('state')

        # Generate tasks based on state
        if state == GitWorkflowState.MODIFIED and self.auto_commit_enabled:
            tasks.append({
                'type': 'commit',
                'priority': 'high',
                'description': 'Commit modified files autonomously',
                'action': self.autonomous_commit
            })

        if state == GitWorkflowState.AHEAD and self.auto_push_enabled:
            tasks.append({
                'type': 'push',
                'priority': 'high',
                'description': 'Push commits to remote repository',
                'action': self.autonomous_push
            })

        if state == GitWorkflowState.BEHIND:
            tasks.append({
                'type': 'pull',
                'priority': 'medium',
                'description': 'Pull latest changes from remote',
                'action': self.autonomous_pull
            })

        # Regular maintenance tasks
        if self.auto_branch_management:
            tasks.append({
                'type': 'branch_cleanup',
                'priority': 'low',
                'description': 'Clean up merged branches',
                'action': self.autonomous_branch_management
            })

        return tasks

    def execute_workflow_cycle(self) -> Dict[str, Any]:
        """Execute complete workflow cycle"""
        cycle_start = datetime.now(timezone.utc)

        self.logger.info("🔄 Starting autonomous workflow cycle")

        # Generate tasks
        tasks = self.generate_workflow_tasks()

        results = {
            'cycle_start': cycle_start.isoformat(),
            'tasks_generated': len(tasks),
            'tasks_completed': 0,
            'tasks_failed': 0,
            'results': []
        }

        # Execute tasks in priority order
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        tasks.sort(key=lambda t: priority_order.get(t['priority'], 3))

        for task in tasks:
            try:
                self.logger.info(f"🚀 Executing {task['type']}: {task['description']}")

                success = task['action']()

                if success:
                    results['tasks_completed'] += 1
                    results['results'].append({
                        'task': task['type'],
                        'status': 'success',
                        'description': task['description']
                    })
                else:
                    results['tasks_failed'] += 1
                    results['results'].append({
                        'task': task['type'],
                        'status': 'failed',
                        'description': task['description']
                    })

            except Exception as e:
                self.logger.error(f"❌ Task {task['type']} failed: {e}")
                results['tasks_failed'] += 1
                results['results'].append({
                    'task': task['type'],
                    'status': 'error',
                    'description': task['description'],
                    'error': str(e)
                })

        # Update cycle completion
        results['cycle_end'] = datetime.now(timezone.utc).isoformat()
        results['duration_seconds'] = (datetime.now(timezone.utc) - cycle_start).total_seconds()

        # Log final status
        self.logger.info(f"✅ Workflow cycle completed: {results['tasks_completed']} success, {results['tasks_failed']} failed")

        return results

    def run_continuous_workflow(self, interval: int = 60):
        """Run continuous autonomous workflow"""
        self.logger.info("🧬 DAIOF Autonomous Git Workflow - CONTINUOUS MODE ACTIVATED")
        self.logger.info(f"⏱️  Check interval: {interval} seconds")
        self.logger.info("="*80)

        cycle_count = 0

        try:
            while True:
                cycle_count += 1
                cycle_start = datetime.now(timezone.utc)

                self.logger.info(f"\n🔄 Cycle {cycle_count} - {cycle_start.strftime('%H:%M:%S UTC')}")

                # Execute workflow cycle
                results = self.execute_workflow_cycle()

                # Log cycle summary
                self.logger.info(f"📊 Cycle Summary:")
                self.logger.info(f"   Duration: {results['duration_seconds']:.1f}s")
                self.logger.info(f"   Tasks: {results['tasks_completed']}/{results['tasks_generated']} completed")
                self.logger.info(f"   Health: K={self.k_state}, Safety={min(self.pillars_scores.values()):.1f}")

                # Save cycle log
                self._save_workflow_log(results)

                # Wait for next cycle
                elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
                sleep_time = max(0, interval - elapsed)

                if sleep_time > 0:
                    self.logger.info(f"⏰ Next cycle in {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.logger.info("\n\n⏹️  Autonomous workflow stopped by user")
            self._generate_final_report()

        except Exception as e:
            self.logger.error(f"❌ Critical error in workflow: {e}")
            self._generate_final_report()

    def _save_workflow_log(self, results: Dict):
        """Save workflow execution log"""
        log_dir = self.repo_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"workflow_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"

        # Load existing logs
        existing_logs = []
        if log_file.exists():
            with open(log_file) as f:
                existing_logs = json.load(f)

        # Add new log
        existing_logs.append(results)

        # Keep only last 100 entries
        if len(existing_logs) > 100:
            existing_logs = existing_logs[-100:]

        # Save
        with open(log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)

    def _generate_final_report(self):
        """Generate final workflow report"""
        report = {
            'end_time': datetime.now(timezone.utc).isoformat(),
            'total_cycles': getattr(self, 'cycle_count', 0),
            'final_health': {
                'k_state': self.k_state,
                'pillars_scores': self.pillars_scores,
                'health_metrics': self.health_metrics
            },
            'haios_compliance': self._check_haios_compliance(),
            'creator_attribution': {
                'creator': 'Nguyễn Đức Cường (alpha_prime_omega)',
                'framework': 'HYPERAI',
                'verification_code': 4287
            }
        }

        report_file = self.repo_path / 'logs' / 'final_workflow_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info("📊 Final workflow report saved")
        self.logger.info(f"🧬 K-State: {self.k_state} | HAIOS Compliant: {report['haios_compliance']}")


def main():
    """Main entry point"""
    workflow = AutonomousGitWorkflow()

    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'status':
            status = workflow.get_git_status()
            print(json.dumps(status, indent=2))
        elif command == 'commit':
            message = sys.argv[2] if len(sys.argv) > 2 else None
            success = workflow.autonomous_commit(message)
            print(f"Commit {'successful' if success else 'failed'}")
        elif command == 'push':
            success = workflow.autonomous_push()
            print(f"Push {'successful' if success else 'failed'}")
        elif command == 'pull':
            success = workflow.autonomous_pull()
            print(f"Pull {'successful' if success else 'failed'}")
        elif command == 'cycle':
            results = workflow.execute_workflow_cycle()
            print(json.dumps(results, indent=2))
        else:
            print("Usage: python autonomous_git_workflow.py [status|commit|push|pull|cycle]")
    else:
        # Run continuous workflow
        workflow.run_continuous_workflow(interval=60)  # Check every minute


if __name__ == '__main__':
    main()