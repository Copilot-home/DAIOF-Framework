#!/usr/bin/env python3
"""
Real-Time Autonomous Task Generator
Continuously generates and executes tasks for organism self-improvement

This system:
- Analyzes current state every second
- Identifies improvement opportunities
- Creates actionable tasks
- Prioritizes and executes
- Learns from outcomes
"""

import os
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml


class TaskPriority:
    """Task priority levels"""
    CRITICAL = 0    # Security, bugs, broken features
    HIGH = 1        # Performance, quality, user experience
    MEDIUM = 2      # Features, enhancements, optimizations
    LOW = 3         # Nice-to-have, cosmetic, future
    

class Task:
    """Autonomous task definition"""
    
    def __init__(self, 
                 title: str,
                 description: str,
                 action: str,
                 priority: int = TaskPriority.MEDIUM,
                 estimated_time: int = 60,
                 dependencies: List[str] = None):
        self.id = f"task_{int(time.time() * 1000)}"
        self.title = title
        self.description = description
        self.action = action  # Shell command or Python code
        self.priority = priority
        self.estimated_time = estimated_time  # seconds
        self.dependencies = dependencies or []
        self.created_at = datetime.utcnow()
        self.status = "pending"  # pending, in_progress, completed, failed
        self.result = None
        self.error = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'action': self.action,
            'priority': self.priority,
            'estimated_time': self.estimated_time,
            'dependencies': self.dependencies,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'result': self.result,
            'error': self.error
        }


class RealtimeTaskGenerator:
    """Generates tasks in real-time based on repository state"""
    
    def __init__(self, repo_path: Path = Path('.')):
        self.repo_path = repo_path
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
        
        # State tracking
        self.last_commit_time = None
        self.last_health_check = None
        self.file_modifications: Dict[str, float] = {}
        
        # Task generation rules
        self.generation_rules = [
            self._check_uncommitted_changes,
            self._check_health_status,
            self._check_code_quality,
            self._check_documentation_coverage,
            self._check_test_coverage,
            self._check_dependencies,
            self._check_issues,
            self._check_prs,
            self._check_performance,
            self._check_security,
        ]
        
        # Load genome for decision making
        self.genome = self._load_genome()
        
        # Metrics
        self.total_tasks_generated = 0
        self.total_tasks_completed = 0
        self.total_tasks_failed = 0
    
    def _load_genome(self) -> Dict:
        """Load organism genome"""
        genome_file = self.repo_path / '.github' / 'DIGITAL_ORGANISM_GENOME.yml'
        if genome_file.exists():
            with open(genome_file) as f:
                return yaml.safe_load(f)
        return {}
    
    def _check_uncommitted_changes(self) -> List[Task]:
        """Check for uncommitted changes"""
        tasks = []
        
        try:
            # Check git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout.strip():
                # There are uncommitted changes
                tasks.append(Task(
                    title="Commit Pending Changes",
                    description="Found uncommitted changes in repository",
                    action="git add -A && git commit -m '🤖 Auto-commit: Real-time updates' && git push",
                    priority=TaskPriority.HIGH,
                    estimated_time=30
                ))
        except Exception as e:
            print(f"Error checking git status: {e}")
        
        return tasks
    
    def _check_health_status(self) -> List[Task]:
        """Check organism health and create improvement tasks"""
        tasks = []
        
        health_file = self.repo_path / 'metrics' / 'latest_health.json'
        
        if health_file.exists():
            with open(health_file) as f:
                health = json.load(f)
                
                overall = health.get('overall_health', 0)
                
                # If health is low, create improvement tasks
                if overall < 0.7:
                    tasks.append(Task(
                        title="Improve Organism Health",
                        description=f"Current health: {overall:.1%}. Need improvement.",
                        action="python3 .github/scripts/health_monitor.py",
                        priority=TaskPriority.HIGH,
                        estimated_time=60
                    ))
                
                # Check individual vital signs
                vitals = health.get('vital_signs', {})
                
                if vitals.get('code_quality', 1.0) < 0.8:
                    tasks.append(Task(
                        title="Improve Code Quality",
                        description="Code quality below 80%",
                        action="black . && isort .",
                        priority=TaskPriority.MEDIUM,
                        estimated_time=45
                    ))
        
        return tasks
    
    def _check_code_quality(self) -> List[Task]:
        """Check code quality and create improvement tasks"""
        tasks = []
        
        # Find Python files that need formatting
        for py_file in self.repo_path.rglob('*.py'):
            if any(x in str(py_file) for x in ['venv', '.venv', 'build', 'dist']):
                continue
            
            # Check if file was modified recently
            mod_time = py_file.stat().st_mtime
            last_checked = self.file_modifications.get(str(py_file), 0)
            
            if mod_time > last_checked:
                tasks.append(Task(
                    title=f"Format {py_file.name}",
                    description=f"Format and optimize {py_file}",
                    action=f"black {py_file} && isort {py_file}",
                    priority=TaskPriority.LOW,
                    estimated_time=10
                ))
                
                self.file_modifications[str(py_file)] = time.time()
        
        return tasks
    
    def _check_documentation_coverage(self) -> List[Task]:
        """Check for missing documentation"""
        tasks = []
        
        # Check for required files
        required_docs = {
            'CONTRIBUTING.md': 'Create contributing guidelines',
            'CODE_OF_CONDUCT.md': 'Create code of conduct',
            'SECURITY.md': 'Create security policy',
            'CHANGELOG.md': 'Create changelog',
            'FAQ.md': 'Create FAQ document',
        }
        
        for doc_file, description in required_docs.items():
            if not (self.repo_path / doc_file).exists():
                tasks.append(Task(
                    title=f"Create {doc_file}",
                    description=description,
                    action=f"python3 .github/scripts/autonomous_developer.py --create-doc {doc_file}",
                    priority=TaskPriority.MEDIUM,
                    estimated_time=120
                ))
        
        return tasks
    
    def _check_test_coverage(self) -> List[Task]:
        """Check test coverage"""
        tasks = []
        
        # Check if tests directory exists
        tests_dir = self.repo_path / 'tests'
        if not tests_dir.exists():
            tasks.append(Task(
                title="Create Tests Directory",
                description="Initialize testing infrastructure",
                action="mkdir -p tests && touch tests/__init__.py",
                priority=TaskPriority.HIGH,
                estimated_time=30
            ))
        
        return tasks
    
    def _check_dependencies(self) -> List[Task]:
        """Check for outdated dependencies"""
        tasks = []
        
        # Check if requirements.txt needs update
        req_file = self.repo_path / 'requirements.txt'
        if req_file.exists():
            # Check age of file
            mod_time = req_file.stat().st_mtime
            age_days = (time.time() - mod_time) / 86400
            
            if age_days > 7:  # Check weekly
                tasks.append(Task(
                    title="Check Dependency Updates",
                    description="Weekly dependency update check",
                    action="pip list --outdated",
                    priority=TaskPriority.MEDIUM,
                    estimated_time=60
                ))
        
        return tasks
    
    def _check_issues(self) -> List[Task]:
        """Check for open issues that can be auto-resolved"""
        tasks = []
        
        # This would integrate with GitHub API
        # For now, placeholder
        
        return tasks
    
    def _check_prs(self) -> List[Task]:
        """Check for PRs that need review"""
        tasks = []
        
        # This would integrate with GitHub API
        # For now, placeholder
        
        return tasks
    
    def _check_performance(self) -> List[Task]:
        """Check performance metrics"""
        tasks = []
        
        # Check if profiling is needed
        # Placeholder for now
        
        return tasks
    
    def _check_security(self) -> List[Task]:
        """Check for security issues"""
        tasks = []
        
        # Check for secrets in code
        # Check for vulnerable dependencies
        # Placeholder for now
        
        return tasks
    
    def generate_tasks(self) -> List[Task]:
        """Generate tasks based on current state"""
        new_tasks = []
        
        # Run all generation rules
        for rule in self.generation_rules:
            try:
                tasks = rule()
                new_tasks.extend(tasks)
            except Exception as e:
                print(f"Error in rule {rule.__name__}: {e}")
        
        # Deduplicate tasks against each other AND against the active queue
        # This prevents spamming the queue with the same pending actions
        seen_titles = {t.title for t in self.task_queue}
        unique_tasks = []
        for task in new_tasks:
            if task.title not in seen_titles:
                seen_titles.add(task.title)
                unique_tasks.append(task)
        
        self.total_tasks_generated += len(unique_tasks)
        
        return unique_tasks
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Prioritize tasks based on multiple factors"""
        # Sort by priority, then estimated time
        return sorted(tasks, key=lambda t: (t.priority, t.estimated_time))
    
    def execute_task(self, task: Task) -> bool:
        """Execute a single task"""
        print(f"\n🚀 Executing: {task.title}")
        print(f"   Description: {task.description}")
        print(f"   Action: {task.action}")
        
        task.status = "in_progress"
        
        try:
            # Execute the action
            result = subprocess.run(
                task.action,
                shell=True,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=task.estimated_time
            )
            
            if result.returncode == 0:
                task.status = "completed"
                task.result = result.stdout
                self.completed_tasks.append(task)
                self.total_tasks_completed += 1
                print(f"   ✅ Success!")
                return True
            else:
                task.status = "failed"
                task.error = result.stderr
                self.failed_tasks.append(task)
                self.total_tasks_failed += 1
                print(f"   ❌ Failed: {result.stderr[:100]}")
                return False
                
        except subprocess.TimeoutExpired:
            task.status = "failed"
            task.error = "Timeout"
            self.failed_tasks.append(task)
            self.total_tasks_failed += 1
            print(f"   ⏰ Timeout!")
            return False
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            self.failed_tasks.append(task)
            self.total_tasks_failed += 1
            print(f"   ❌ Error: {e}")
            return False
    
    def save_task_log(self):
        """Save task execution log"""
        log_dir = self.repo_path / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"tasks_{datetime.utcnow().strftime('%Y%m%d')}.json"
        
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_generated': self.total_tasks_generated,
            'total_completed': self.total_tasks_completed,
            'total_failed': self.total_tasks_failed,
            'pending': [t.to_dict() for t in self.task_queue],
            'completed': [t.to_dict() for t in self.completed_tasks[-10:]],  # Last 10
            'failed': [t.to_dict() for t in self.failed_tasks[-10:]],  # Last 10
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def run_continuous(self, interval: int = 10):
        """Run continuous task generation and execution"""
        print("🧬 Real-Time Autonomous Task Generator ACTIVE")
        print(f"⏱️  Interval: {interval} seconds")
        print(f"📍 Repository: {self.repo_path}")
        print("="*70)
        
        cycle = 0
        
        try:
            while True:
                cycle += 1
                print(f"\n🔄 Cycle {cycle} - {datetime.utcnow().strftime('%H:%M:%S')}")
                
                # Generate new tasks
                new_tasks = self.generate_tasks()
                
                if new_tasks:
                    print(f"   📋 Generated {len(new_tasks)} new tasks")
                    
                    # Add to queue
                    self.task_queue.extend(new_tasks)
                    
                    # Prioritize
                    self.task_queue = self.prioritize_tasks(self.task_queue)
                    
                    # Execute top priority task
                    if self.task_queue:
                        task = self.task_queue.pop(0)
                        self.execute_task(task)
                else:
                    print("   ℹ️  No new tasks generated")
                
                # Show stats
                print(f"\n   📊 Stats:")
                print(f"      Queue: {len(self.task_queue)} tasks")
                print(f"      Completed: {self.total_tasks_completed}")
                print(f"      Failed: {self.total_tasks_failed}")
                
                # Save log
                self.save_task_log()
                
                # Wait for next cycle
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping autonomous task generator...")
            print(f"📊 Final Stats:")
            print(f"   Total Generated: {self.total_tasks_generated}")
            print(f"   Total Completed: {self.total_tasks_completed}")
            print(f"   Total Failed: {self.total_tasks_failed}")
            print(f"   Success Rate: {self.total_tasks_completed/(self.total_tasks_completed+self.total_tasks_failed)*100:.1f}%")


def main():
    """Main entry point"""
    generator = RealtimeTaskGenerator()
    generator.run_continuous(interval=10)  # Check every 10 seconds


if __name__ == '__main__':
    main()
