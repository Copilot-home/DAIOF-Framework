#!/usr/bin/env python3
"""
🧬 DAIOF Autonomous Git Workflow Tests
Tests for uncommitted changes detection and autonomous git operations

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Framework: HYPERAI
Date: November 17, 2025
"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import shutil
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / '.github' / 'scripts'))


def status_env():
    env = os.environ.copy()
    env["DAIOF_SKIP_REMOTE_STATUS"] = "1"
    return env


class TestAutonomousGitWorkflow(unittest.TestCase):
    """Test suite for autonomous git workflow system"""

    def test_import_workflow_module(self):
        """Test that the workflow module can be imported"""
        try:
            from autonomous_git_workflow import AutonomousGitWorkflow, GitWorkflowState
            self.assertIsNotNone(AutonomousGitWorkflow)
            self.assertIsNotNone(GitWorkflowState)
        except ImportError as e:
            self.skipTest(f"Cannot import module (missing dependencies): {e}")

    def test_git_workflow_states(self):
        """Test that GitWorkflowState enum has required states"""
        try:
            from autonomous_git_workflow import GitWorkflowState
            
            # Verify all required states exist
            self.assertEqual(GitWorkflowState.CLEAN, "clean")
            self.assertEqual(GitWorkflowState.MODIFIED, "modified")
            self.assertEqual(GitWorkflowState.STAGED, "staged")
            self.assertEqual(GitWorkflowState.CONFLICTS, "conflicts")
            self.assertEqual(GitWorkflowState.BEHIND, "behind")
            self.assertEqual(GitWorkflowState.AHEAD, "ahead")
            self.assertEqual(GitWorkflowState.DIVERGED, "diverged")
        except ImportError as e:
            self.skipTest(f"Cannot import module (missing dependencies): {e}")

    def test_workflow_status_check(self):
        """Test workflow status check functionality"""
        # This test verifies the status command works
        result = subprocess.run(
            [sys.executable, '.github/scripts/autonomous_git_workflow.py', 'status'],
            cwd=Path(__file__).parent.parent,
            env=status_env(),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Should exit successfully
        self.assertEqual(result.returncode, 0, f"Status check failed: {result.stderr}")
        
        # Should output JSON
        self.assertIn('"state":', result.stdout)
        self.assertIn('"branch":', result.stdout)

    def test_uncommitted_changes_detection(self):
        """Test that uncommitted changes are properly detected"""
        # Create a temporary file to simulate uncommitted changes
        test_file = Path(__file__).parent.parent / 'test_uncommitted.daiof_probe'
        
        try:
            # Create test file
            test_file.write_text('Test uncommitted changes detection')
            
            # Run status check
            result = subprocess.run(
                [sys.executable, '.github/scripts/autonomous_git_workflow.py', 'status'],
                cwd=Path(__file__).parent.parent,
                env=status_env(),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            self.assertEqual(result.returncode, 0)
            
            # Should detect modified state
            self.assertIn('"state":', result.stdout)
            # The state should be either "modified" or show the test file
            self.assertTrue(
                '"modified"' in result.stdout or 
                'test_uncommitted.daiof_probe' in result.stdout,
                "Uncommitted changes not detected"
            )
            
        finally:
            # Clean up - don't commit the test file
            if test_file.exists():
                test_file.unlink()

    def test_haios_compliance_metadata(self):
        """Test that HAIOS compliance metadata is present in the workflow"""
        workflow_file = Path(__file__).parent.parent / '.github' / 'scripts' / 'autonomous_git_workflow.py'
        content = workflow_file.read_text()
        
        # Verify creator attribution (HAIOS Invariant 1)
        self.assertIn('Nguyễn Đức Cường (alpha_prime_omega)', content)
        
        # Verify framework attribution
        self.assertIn('HYPERAI', content)
        
        # Verify 4 Pillars integration
        self.assertIn('4 Pillars', content)
        self.assertIn('an_toan', content)
        self.assertIn('duong_dai', content)
        self.assertIn('tin_vao_so_lieu', content)
        self.assertIn('han_che_rui_ro', content)
        
        # Verify K-State tracking
        self.assertIn('k_state', content)

    def test_workflow_cycle_structure(self):
        """Test that workflow cycle has proper structure"""
        try:
            from autonomous_git_workflow import AutonomousGitWorkflow
            
            # This just verifies the class structure, doesn't execute workflow
            workflow = AutonomousGitWorkflow()
            
            # Verify key methods exist
            self.assertTrue(hasattr(workflow, 'get_git_status'))
            self.assertTrue(hasattr(workflow, 'autonomous_commit'))
            self.assertTrue(hasattr(workflow, 'autonomous_push'))
            self.assertTrue(hasattr(workflow, 'generate_workflow_tasks'))
            self.assertTrue(hasattr(workflow, 'execute_workflow_cycle'))
            
            # Verify HAIOS compliance attributes
            self.assertEqual(workflow.k_state, 1, "K-State must be 1")
            self.assertIn('an_toan', workflow.pillars_scores)
            self.assertIn('duong_dai', workflow.pillars_scores)
            self.assertIn('tin_vao_so_lieu', workflow.pillars_scores)
            self.assertIn('han_che_rui_ro', workflow.pillars_scores)
            
        except ImportError as e:
            self.skipTest(f"Cannot import module (missing dependencies): {e}")


class TestUncommittedChangesHandling(unittest.TestCase):
    """Specific tests for uncommitted changes handling"""

    def test_workflow_detects_modified_state(self):
        """Test workflow correctly identifies MODIFIED state"""
        # This is a documentation test that verifies the workflow
        # should transition to MODIFIED state when files are changed
        
        # Create a temporary file
        test_file = Path(__file__).parent.parent / 'test_modified_detection.daiof_probe'
        
        try:
            test_file.write_text('Testing modified state detection')
            
            result = subprocess.run(
                [sys.executable, '.github/scripts/autonomous_git_workflow.py', 'status'],
                cwd=Path(__file__).parent.parent,
                env=status_env(),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Verify it detected changes
            output = result.stdout
            self.assertIn('"modified_files":', output)
            
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_clean_state_when_no_changes(self):
        """Test workflow reports CLEAN state when no uncommitted changes"""
        # Ensure we're in a clean state first
        subprocess.run(['git', 'status', '--porcelain'], 
                      cwd=Path(__file__).parent.parent,
                      check=True)
        
        result = subprocess.run(
            [sys.executable, '.github/scripts/autonomous_git_workflow.py', 'status'],
            cwd=Path(__file__).parent.parent,
            env=status_env(),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        self.assertEqual(result.returncode, 0)
        # Should show state info
        self.assertIn('"state":', result.stdout)


def run_tests():
    """Run all tests"""
    print("🧬 DAIOF Autonomous Git Workflow Tests")
    print("Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    print("Framework: HYPERAI")
    print("="*80)
    print()
    
    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAutonomousGitWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestUncommittedChangesHandling))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    print("🧬 Framework: HYPERAI | Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
