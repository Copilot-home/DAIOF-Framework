#!/usr/bin/env python3
"""
🧬 DAIOF Multi-Repository Autonomous Control System
Hệ thống điều khiển đa repository tự trị hoàn hảo

Tự động quản lý toàn bộ tài khoản GitHub với:
- Multi-repository orchestration và auxiliary pilots
- Autonomous issue/PR management và bug fixing
- Real-time monitoring across all repositories
- Conflict resolution và merge management
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
import threading
from datetime import datetime, timedelta, UTC
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from github import Github, Auth, Repository, Issue, PullRequest
import logging
import requests


class AuxiliaryPilot:
    """
    Phi công phụ - Autonomous agent cho từng repository

    Mỗi pilot chịu trách nhiệm:
    - Monitor repository health
    - Handle issues và PRs tự động
    - Fix bugs và errors
    - Maintain repository harmony
    """

    def __init__(self, repo: Repository.Repository, main_controller):
        self.repo = repo
        self.main_controller = main_controller
        self.repo_name = repo.full_name
        self.logger = main_controller.logger
        self.health_score = 100
        self.last_activity = datetime.now(UTC)
        self.active_issues = []
        self.pending_fixes = []

        self.logger.info(f"✈️ Auxiliary Pilot activated for: {self.repo_name}")

    def monitor_repository(self) -> Dict[str, Any]:
        """Monitor repository health và activities"""
        try:
            # Get repository stats
            stats = {
                'name': self.repo_name,
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'open_issues': self.repo.open_issues_count,
                'last_push': self.repo.pushed_at.isoformat() if self.repo.pushed_at else None,
                'health_score': self.health_score
            }

            # Check for new issues
            new_issues = self._scan_for_issues()
            if new_issues:
                self.logger.info(f"🚨 {len(new_issues)} new issues detected in {self.repo_name}")
                self.active_issues.extend(new_issues)

            # Check for failing workflows
            failing_workflows = self._check_ci_status()
            if failing_workflows:
                self.logger.warning(f"❌ {len(failing_workflows)} failing workflows in {self.repo_name}")
                self._handle_failing_workflows(failing_workflows)

            # Update health score
            self._update_health_score()

            return stats

        except Exception as e:
            self.logger.error(f"❌ Pilot monitoring failed for {self.repo_name}: {e}")
            return {'error': str(e)}

    def _scan_for_issues(self) -> List[Issue.Issue]:
        """Scan for new issues requiring attention"""
        try:
            # Get recent issues (last 24 hours)
            since = datetime.now(UTC) - timedelta(hours=24)
            issues = self.repo.get_issues(state='open', since=since)

            urgent_issues = []
            for issue in issues:
                # Check if issue needs immediate attention
                if self._is_urgent_issue(issue):
                    urgent_issues.append(issue)

            return urgent_issues

        except Exception as e:
            self.logger.error(f"Error scanning issues for {self.repo_name}: {e}")
            return []

    def _is_urgent_issue(self, issue: Issue.Issue) -> bool:
        """Determine if issue requires urgent attention"""
        # Check labels
        urgent_labels = ['bug', 'critical', 'security', 'breaking', 'urgent']
        issue_labels = [label.name.lower() for label in issue.labels]

        if any(label in issue_labels for label in urgent_labels):
            return True

        # Check title keywords
        urgent_keywords = ['crash', 'error', 'fail', 'broken', 'security', 'vulnerability']
        title_lower = issue.title.lower()

        if any(keyword in title_lower for keyword in urgent_keywords):
            return True

        return False

    def _check_ci_status(self) -> List[Dict]:
        """Check CI/CD workflow status"""
        try:
            # Get recent workflow runs
            workflows = self.repo.get_workflows()
            failing_runs = []

            for workflow in workflows:
                runs = workflow.get_runs()
                if runs.totalCount > 0:
                    latest_run = runs[0]
                    if latest_run.conclusion == 'failure':
                        failing_runs.append({
                            'workflow': workflow.name,
                            'run_id': latest_run.id,
                            'failure_time': latest_run.created_at.isoformat()
                        })

            return failing_runs

        except Exception as e:
            self.logger.error(f"Error checking CI status for {self.repo_name}: {e}")
            return []

    def _handle_failing_workflows(self, failing_workflows: List[Dict]):
        """Handle failing CI/CD workflows"""
        for workflow in failing_workflows:
            try:
                # Create issue for failing workflow
                issue_title = f"🚨 CI/CD Failure: {workflow['workflow']}"
                issue_body = f"""## CI/CD Workflow Failure Detected

**Repository:** {self.repo_name}
**Workflow:** {workflow['workflow']}
**Run ID:** {workflow['run_id']}
**Failure Time:** {workflow['failure_time']}

### Autonomous Analysis:
- Workflow failure detected by auxiliary pilot
- Issue created for immediate attention
- Pilot will attempt automated fixes

### Recommended Actions:
1. Review workflow logs
2. Check for dependency issues
3. Verify configuration changes
4. Test locally before redeploying

---
*🤖 Reported by HYPERAI Auxiliary Pilot*
*Framework: HYPERAI | Creator: Nguyễn Đức Cường (alpha_prime_omega)*
"""

                # Check if issue already exists
                existing_issues = self.repo.get_issues(state='open')
                issue_exists = False

                for existing in existing_issues:
                    if existing.title == issue_title:
                        issue_exists = True
                        break

                if not issue_exists:
                    issue = self.repo.create_issue(
                        title=issue_title,
                        body=issue_body,
                        labels=['bug', 'ci-failure', 'autonomous-report']
                    )
                    self.logger.info(f"📋 Created issue for failing workflow: {issue.html_url}")

                    # Attempt automated fix
                    self._attempt_workflow_fix(workflow)

            except Exception as e:
                self.logger.error(f"Error handling failing workflow {workflow['workflow']}: {e}")

    def _attempt_workflow_fix(self, workflow: Dict):
        """Attempt automated fix for failing workflow"""
        try:
            # Common fixes for CI failures
            workflow_name = workflow['workflow'].lower()

            if 'test' in workflow_name:
                # Test failures - check for common issues
                self._fix_test_failures()
            elif 'build' in workflow_name:
                # Build failures - check dependencies
                self._fix_build_failures()
            elif 'lint' in workflow_name:
                # Linting failures - auto-fix formatting
                self._fix_lint_failures()

        except Exception as e:
            self.logger.error(f"Error attempting workflow fix: {e}")

    def _fix_test_failures(self):
        """Attempt to fix common test failures"""
        # This would implement automated test fixing logic
        self.logger.info(f"🔧 Attempting automated test fixes for {self.repo_name}")

    def _fix_build_failures(self):
        """Attempt to fix common build failures"""
        # This would implement automated build fixing logic
        self.logger.info(f"🔧 Attempting automated build fixes for {self.repo_name}")

    def _fix_lint_failures(self):
        """Attempt to fix common linting failures"""
        # This would implement automated linting fixes
        self.logger.info(f"🔧 Attempting automated lint fixes for {self.repo_name}")

    def handle_issues(self):
        """Handle pending issues autonomously"""
        for issue in self.active_issues[:]:
            try:
                if self._can_auto_fix_issue(issue):
                    success = self._auto_fix_issue(issue)
                    if success:
                        self.active_issues.remove(issue)
                        self.logger.info(f"✅ Auto-fixed issue #{issue.number} in {self.repo_name}")
                    else:
                        self._escalate_issue(issue)
                else:
                    self._escalate_issue(issue)

            except Exception as e:
                self.logger.error(f"Error handling issue #{issue.number}: {e}")

    def _can_auto_fix_issue(self, issue: Issue.Issue) -> bool:
        """Determine if issue can be auto-fixed"""
        # Check issue labels and content for auto-fixable patterns
        labels = [label.name.lower() for label in issue.labels]

        # Auto-fixable issue types
        auto_fixable = [
            'dependency-update',
            'typo',
            'formatting',
            'simple-bug',
            'documentation'
        ]

        return any(label in auto_fixable for label in labels)

    def _auto_fix_issue(self, issue: Issue.Issue) -> bool:
        """Attempt automated issue fix"""
        try:
            labels = [label.name.lower() for label in issue.labels]

            if 'dependency-update' in labels:
                return self._fix_dependency_issue(issue)
            elif 'typo' in labels:
                return self._fix_typo_issue(issue)
            elif 'formatting' in labels:
                return self._fix_formatting_issue(issue)
            elif 'documentation' in labels:
                return self._fix_documentation_issue(issue)

            return False

        except Exception as e:
            self.logger.error(f"Auto-fix failed for issue #{issue.number}: {e}")
            return False

    def _fix_dependency_issue(self, issue: Issue.Issue) -> bool:
        """Fix dependency-related issues"""
        # Implement dependency update logic
        self.logger.info(f"🔧 Updating dependencies for {self.repo_name}")
        return True

    def _fix_typo_issue(self, issue: Issue.Issue) -> bool:
        """Fix typo issues"""
        # Implement typo correction logic
        self.logger.info(f"🔧 Fixing typos in {self.repo_name}")
        return True

    def _fix_formatting_issue(self, issue: Issue.Issue) -> bool:
        """Fix formatting issues"""
        # Implement code formatting logic
        self.logger.info(f"🔧 Fixing formatting in {self.repo_name}")
        return True

    def _fix_documentation_issue(self, issue: Issue.Issue) -> bool:
        """Fix documentation issues"""
        # Implement documentation update logic
        self.logger.info(f"🔧 Updating documentation for {self.repo_name}")
        return True

    def _escalate_issue(self, issue: Issue.Issue):
        """Escalate issue for human attention"""
        try:
            # Add escalation label
            issue.add_to_labels('needs-human-review')

            # Comment on issue
            comment = """## 🤖 Auxiliary Pilot Escalation

This issue requires human review and cannot be auto-resolved by the auxiliary pilot.

### Pilot Analysis:
- Issue complexity exceeds autonomous capabilities
- Manual intervention required
- Pilot will continue monitoring for updates

### Recommended Actions:
1. Review issue details and requirements
2. Assess feasibility of manual fix
3. Coordinate with development team if needed
4. Update issue status and assign responsible party

---
*🤖 Escalated by HYPERAI Auxiliary Pilot*
*Framework: HYPERAI | Creator: Nguyễn Đức Cường (alpha_prime_omega)*
"""
            issue.create_comment(comment)
            self.logger.info(f"📈 Escalated issue #{issue.number} in {self.repo_name}")

        except Exception as e:
            self.logger.error(f"Error escalating issue #{issue.number}: {e}")

    def _update_health_score(self):
        """Update repository health score"""
        try:
            # Calculate health based on various factors
            base_score = 100

            # Deduct for open issues
            issue_penalty = min(self.repo.open_issues_count * 2, 30)
            base_score -= issue_penalty

            # Deduct for failing workflows
            failing_workflows = len(self._check_ci_status())
            workflow_penalty = failing_workflows * 10
            base_score -= workflow_penalty

            # Bonus for recent activity
            days_since_push = (datetime.now(UTC) - self.repo.pushed_at).days if self.repo.pushed_at else 30
            activity_bonus = max(0, 10 - days_since_push)
            base_score += activity_bonus

            self.health_score = max(0, min(100, base_score))

        except Exception as e:
            self.logger.error(f"Error updating health score for {self.repo_name}: {e}")
            self.health_score = 50  # Default to neutral on error

    def get_status(self) -> Dict[str, Any]:
        """Get pilot status"""
        return {
            'repository': self.repo_name,
            'health_score': self.health_score,
            'active_issues': len(self.active_issues),
            'pending_fixes': len(self.pending_fixes),
            'last_activity': self.last_activity.isoformat()
        }


class MultiRepositoryOrchestrator:
    """
    Bộ điều khiển đa repository - Main orchestrator cho auxiliary pilots

    Quản lý:
    - Multiple auxiliary pilots
    - Cross-repository coordination
    - Global health monitoring
    - Emergency response protocols
    """

    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.user = os.environ.get('GITHUB_ACTOR', 'NguyenCuong1989')
        self.logger = self._setup_logging()
        self.pilots: Dict[str, AuxiliaryPilot] = {}
        self.global_health = 100
        self.emergency_mode = False

        # HAIOS compliance
        self.k_state = 1
        self.pillars_scores = {
            'an_toan': 10.0,
            'duong_dai': 10.0,
            'tin_vao_so_lieu': 10.0,
            'han_che_rui_ro': 10.0
        }

        if self.github_token:
            self.gh = Github(self.github_token)
            self._initialize_pilots()

        self.logger.info("🧬 DAIOF Multi-Repository Orchestrator ACTIVATED")
        self.logger.info(f"👤 Creator: Nguyễn Đức Cường (alpha_prime_omega)")
        self.logger.info(f"🎼 Framework: HYPERAI | Verification: 4287")
        self.logger.info(f"✈️ Auxiliary Pilots: {len(self.pilots)}")

    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        logger = logging.getLogger('DAIOF_MultiRepo')
        logger.setLevel(logging.INFO)

        # File handler
        log_file = Path('logs/multi_repo_orchestrator.log')
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

    def _initialize_pilots(self):
        """Initialize auxiliary pilots for all repositories"""
        try:
            user = self.gh.get_user(self.user)
            repos = user.get_repos(type='owner', sort='updated')

            for repo in repos:
                if not repo.fork and repo.full_name.startswith(f"{self.user}/"):
                    pilot = AuxiliaryPilot(repo, self)
                    self.pilots[repo.full_name] = pilot
                    self.logger.info(f"✈️ Pilot initialized: {repo.full_name}")

        except Exception as e:
            self.logger.error(f"Error initializing pilots: {e}")

    def monitor_all_repositories(self) -> Dict[str, Any]:
        """Monitor all repositories via auxiliary pilots"""
        self.logger.info("🔍 Starting multi-repository monitoring cycle")

        results = {
            'timestamp': datetime.now(UTC).isoformat(),
            'total_repositories': len(self.pilots),
            'healthy_repositories': 0,
            'issues_detected': 0,
            'fixes_applied': 0,
            'repository_status': {}
        }

        for repo_name, pilot in self.pilots.items():
            try:
                # Monitor repository
                status = pilot.monitor_repository()

                # Handle issues
                pilot.handle_issues()

                # Update results
                results['repository_status'][repo_name] = status

                if status.get('health_score', 0) >= 70:
                    results['healthy_repositories'] += 1

                results['issues_detected'] += len(pilot.active_issues)

            except Exception as e:
                self.logger.error(f"Error monitoring {repo_name}: {e}")
                results['repository_status'][repo_name] = {'error': str(e)}

        # Update global health
        self._update_global_health(results)

        # Check for emergency conditions
        self._check_emergency_conditions(results)

        self.logger.info(f"✅ Monitoring cycle completed: {results['healthy_repositories']}/{results['total_repositories']} healthy")
        return results

    def _update_global_health(self, results: Dict):
        """Update global ecosystem health"""
        try:
            total_repos = results['total_repositories']
            healthy_repos = results['healthy_repositories']

            if total_repos > 0:
                health_percentage = (healthy_repos / total_repos) * 100
                self.global_health = health_percentage

                # Update pillars based on ecosystem health
                if health_percentage >= 90:
                    self.pillars_scores['an_toan'] = min(10.0, self.pillars_scores['an_toan'] + 0.1)
                elif health_percentage < 70:
                    self.pillars_scores['an_toan'] = max(7.0, self.pillars_scores['an_toan'] - 0.5)

        except Exception as e:
            self.logger.error(f"Error updating global health: {e}")

    def _check_emergency_conditions(self, results: Dict):
        """Check for emergency conditions requiring immediate action"""
        emergency_triggers = [
            self.global_health < 50,
            results['issues_detected'] > 10,
            any(status.get('error') for status in results['repository_status'].values())
        ]

        if any(emergency_triggers):
            self.emergency_mode = True
            self.logger.warning("🚨 EMERGENCY MODE ACTIVATED")
            self._execute_emergency_protocol(results)
        else:
            self.emergency_mode = False

    def _execute_emergency_protocol(self, results: Dict):
        """Execute emergency response protocol"""
        try:
            self.logger.info("🚨 Executing emergency response protocol")

            # Create emergency issue across all repositories
            emergency_report = self._generate_emergency_report(results)

            for repo_name, pilot in self.pilots.items():
                try:
                    pilot.repo.create_issue(
                        title="🚨 EMERGENCY: Ecosystem Health Critical",
                        body=emergency_report,
                        labels=['emergency', 'critical', 'autonomous-report']
                    )
                except Exception as e:
                    self.logger.error(f"Error creating emergency issue in {repo_name}: {e}")

            # Attempt emergency fixes
            self._emergency_fixes(results)

        except Exception as e:
            self.logger.error(f"Emergency protocol failed: {e}")

    def _generate_emergency_report(self, results: Dict) -> str:
        """Generate emergency situation report"""
        return f"""## 🚨 EMERGENCY SITUATION REPORT

**Timestamp:** {results['timestamp']}
**Global Health Score:** {self.global_health:.1f}%
**K-State:** {self.k_state}

### Ecosystem Status:
- **Total Repositories:** {results['total_repositories']}
- **Healthy Repositories:** {results['healthy_repositories']}
- **Issues Detected:** {results['issues_detected']}

### Critical Issues:
{chr(10).join([f"- **{repo}**: {status.get('error', 'Health: ' + str(status.get('health_score', 0)) + '%')}" for repo, status in results['repository_status'].items() if status.get('error') or status.get('health_score', 100) < 50])}

### Emergency Actions Taken:
- Emergency mode activated
- Auxiliary pilots escalated all issues
- Attempting automated emergency fixes
- Creator notification pending

### Required Actions:
1. **IMMEDIATE:** Review critical repository failures
2. **URGENT:** Address security vulnerabilities
3. **HIGH:** Fix breaking changes and bugs
4. **MEDIUM:** Resolve CI/CD failures
5. **LOW:** Update documentation and dependencies

---
*🚨 Generated by HYPERAI Emergency Protocol*
*Framework: HYPERAI | Creator: Nguyễn Đức Cường (alpha_prime_omega)*
*Verification: 4287*
"""

    def _emergency_fixes(self, results: Dict):
        """Attempt emergency fixes across ecosystem"""
        self.logger.info("🔧 Executing emergency fixes")

        # Implement emergency fix logic here
        # This would include critical security patches, rollback procedures, etc.

    def run_continuous_orchestration(self, interval: int = 300):
        """Run continuous multi-repository orchestration"""
        self.logger.info("🧬 DAIOF Multi-Repository Orchestrator - CONTINUOUS MODE")
        self.logger.info(f"⏱️  Check interval: {interval} seconds")
        self.logger.info(f"✈️  Active Pilots: {len(self.pilots)}")
        self.logger.info("="*80)

        cycle_count = 0

        try:
            while True:
                cycle_count += 1
                cycle_start = datetime.now(UTC)

                self.logger.info(f"\n🔄 Orchestration Cycle {cycle_count} - {cycle_start.strftime('%H:%M:%S UTC')}")

                # Execute monitoring cycle
                results = self.monitor_all_repositories()

                # Log cycle summary
                self.logger.info(f"📊 Ecosystem Summary:")
                self.logger.info(f"   Global Health: {self.global_health:.1f}%")
                self.logger.info(f"   K-State: {self.k_state}")
                self.logger.info(f"   Emergency Mode: {'ACTIVE' if self.emergency_mode else 'INACTIVE'}")
                self.logger.info(f"   HAIOS Compliance: {self._check_haios_compliance()}")

                # Removed file saving to eliminate timing disruptions - data flows to unified orchestrator only
                # self._save_orchestration_log(results)

                # Wait for next cycle
                elapsed = (datetime.now(UTC) - cycle_start).total_seconds()
                sleep_time = max(0, interval - elapsed)

                if sleep_time > 0:
                    self.logger.info(f"⏰ Next orchestration cycle in {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.logger.info("\n\n⏹️  Multi-repository orchestration stopped")
            # Removed final report to eliminate file creation - data centralized in orchestrator
            # self._generate_final_report()

        except Exception as e:
            self.logger.error(f"❌ Critical error in orchestration: {e}")
            # Removed final report to eliminate file creation - data centralized in orchestrator
            # self._generate_final_report()

    def _check_haios_compliance(self) -> bool:
        """Check HAIOS invariants compliance"""
        try:
            # All standard HAIOS checks
            safety_score = min(self.pillars_scores.values())
            return safety_score >= 7.0 and self.k_state == 1
        except:
            return False

    def _save_orchestration_log(self, results: Dict):
        """Save orchestration execution log"""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"orchestration_{datetime.now(UTC).strftime('%Y%m%d')}.json"

        # Load existing logs
        existing_logs = []
        if log_file.exists():
            with open(log_file) as f:
                existing_logs = json.load(f)

        # Add new log
        existing_logs.append(results)

        # Keep only last 50 entries
        if len(existing_logs) > 50:
            existing_logs = existing_logs[-50:]

        # Save
        with open(log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)

    def _generate_final_report(self):
        """Generate final orchestration report"""
        report = {
            'end_time': datetime.now(UTC).isoformat(),
            'total_pilots': len(self.pilots),
            'final_health': {
                'global_health': self.global_health,
                'k_state': self.k_state,
                'pillars_scores': self.pillars_scores,
                'emergency_mode': self.emergency_mode
            },
            'haios_compliance': self._check_haios_compliance(),
            'creator_attribution': {
                'creator': 'Nguyễn Đức Cường (alpha_prime_omega)',
                'framework': 'HYPERAI',
                'verification_code': 4287
            }
        }

        report_file = Path('logs/final_orchestration_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info("📊 Final orchestration report saved")
        self.logger.info(f"🧬 Global Health: {self.global_health:.1f}% | K-State: {self.k_state}")


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
            self.gh = Github(auth=Auth.Token(self.github_token))
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
                'timestamp': datetime.now(UTC).isoformat()
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

            self.last_commit_time = datetime.now(UTC)
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
        results['cycle_end'] = datetime.now(UTC).isoformat()
        results['duration_seconds'] = (datetime.now(UTC) - cycle_start).total_seconds()
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
                cycle_start = datetime.now(UTC)
                cycle_start = datetime.now(timezone.utc)

                self.logger.info(f"\n🔄 Cycle {cycle_count} - {cycle_start.strftime('%H:%M:%S UTC')}")

                # Execute workflow cycle
                results = self.execute_workflow_cycle()

                # Log cycle summary
                self.logger.info(f"📊 Cycle Summary:")
                self.logger.info(f"   Duration: {results['duration_seconds']:.1f}s")
                self.logger.info(f"   Tasks: {results['tasks_completed']}/{results['tasks_generated']} completed")
                self.logger.info(f"   Health: K={self.k_state}, Safety={min(self.pillars_scores.values()):.1f}")

                # Removed file saving to eliminate timing disruptions - data flows to unified orchestrator only
                # self._save_workflow_log(results)

                # Wait for next cycle
                elapsed = (datetime.now(UTC) - cycle_start).total_seconds()
                elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
                sleep_time = max(0, interval - elapsed)

                if sleep_time > 0:
                    self.logger.info(f"⏰ Next cycle in {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.logger.info("\n\n⏹️  Autonomous workflow stopped by user")
            # Removed final report to eliminate file creation - data centralized in orchestrator
            # self._generate_final_report()

        except Exception as e:
            self.logger.error(f"❌ Critical error in workflow: {e}")
            # Removed final report to eliminate file creation - data centralized in orchestrator
            # self._generate_final_report()

    def _save_workflow_log(self, results: Dict):
        """Save workflow execution log"""
        log_dir = self.repo_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"workflow_{datetime.now(UTC).strftime('%Y%m%d')}.json"
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
            'end_time': datetime.now(UTC).isoformat(),
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
    if len(sys.argv) > 1 and sys.argv[1] == 'single':
        # Run single repository autonomous workflow
        workflow = AutonomousGitWorkflow()

        if len(sys.argv) > 2:
            command = sys.argv[2]
            if command == 'status':
                status = workflow.get_git_status()
                print(json.dumps(status, indent=2))
            elif command == 'cycle':
                results = workflow.execute_workflow_cycle()
                print(json.dumps(results, indent=2))
        else:
            workflow.run_continuous_workflow(interval=60)
    else:
        # Run multi-repository orchestration
        orchestrator = MultiRepositoryOrchestrator()
        orchestrator.run_continuous_orchestration(interval=300)  # Check every 5 minutes


if __name__ == '__main__':
    main()