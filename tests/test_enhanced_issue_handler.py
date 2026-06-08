#!/usr/bin/env python3
"""
Tests for Enhanced Issue Handler
Powered by HYPERAI Framework
Creator: Nguyễn Đức Cường (alpha_prime_omega)
Original Creation: October 30, 2025
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Add parent directory to path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.join(repo_root, '.github', 'scripts'))

# Import the handler
try:
    from enhanced_issue_handler import EnhancedIssueHandler
except ImportError:
    # Try alternative import path
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "enhanced_issue_handler",
        os.path.join(repo_root, '.github', 'scripts', 'enhanced_issue_handler.py')
    )
    enhanced_issue_handler = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(enhanced_issue_handler)
    EnhancedIssueHandler = enhanced_issue_handler.EnhancedIssueHandler


class TestIssueClassification(unittest.TestCase):
    """Test issue classification logic"""
    
    def setUp(self):
        """Set up test handler"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': '', 'DRY_RUN': 'true'}):
            self.handler = EnhancedIssueHandler()
    
    def test_classify_security_issue(self):
        """Test security issue detection"""
        title = "Security vulnerability in authentication"
        body = "Found a critical security issue with SQL injection"
        
        result = self.handler.classify_issue(title, body)
        
        self.assertEqual(result['category'], 'security')
        self.assertEqual(result['priority'], 'critical')
        self.assertIn('security', result['labels'])
        self.assertIn('priority: critical', result['labels'])
        self.assertGreater(result['confidence'], 0.5)
    
    def test_classify_bug_issue(self):
        """Test bug issue detection"""
        title = "Bug: Application crashes on startup"
        body = "The app crashes with error message when I try to start it"
        
        result = self.handler.classify_issue(title, body)
        
        self.assertEqual(result['category'], 'bug')
        self.assertIn('bug', result['labels'])
        self.assertIn(result['priority'], ['high', 'critical'])
    
    def test_classify_feature_request(self):
        """Test feature request detection"""
        title = "Feature request: Add new enhancement"
        body = "It would be great to add support for this feature"
        
        result = self.handler.classify_issue(title, body)
        
        self.assertEqual(result['category'], 'feature')
        self.assertEqual(result['priority'], 'medium')
        self.assertIn('feature', result['labels'])
    
    def test_classify_documentation_issue(self):
        """Test documentation issue detection"""
        title = "Documentation improvement needed"
        body = "The README needs better examples and guide"
        
        result = self.handler.classify_issue(title, body)
        
        self.assertEqual(result['category'], 'documentation')
        # Priority can be low or medium depending on keywords
        self.assertIn(result['priority'], ['low', 'medium'])
        self.assertIn('documentation', result['labels'])
    
    def test_classify_question(self):
        """Test question detection"""
        title = "Question: How to use this feature?"
        body = "I need help understanding how to use this"
        
        result = self.handler.classify_issue(title, body)
        
        self.assertEqual(result['category'], 'question')
        # Priority can be low or medium depending on keywords
        self.assertIn(result['priority'], ['low', 'medium'])
        self.assertIn('question', result['labels'])
    
    def test_classify_performance_issue(self):
        """Test performance issue detection"""
        title = "Performance: Very slow execution"
        body = "The application is running extremely slow, need optimization"
        
        result = self.handler.classify_issue(title, body)
        
        self.assertEqual(result['category'], 'performance')
        self.assertIn('performance', result['labels'])
    
    def test_classify_empty_body(self):
        """Test classification with empty body"""
        title = "Bug report"
        body = ""
        
        result = self.handler.classify_issue(title, body)
        
        self.assertIn('category', result)
        self.assertIn('priority', result)
        self.assertIn('labels', result)
        self.assertGreaterEqual(result['confidence'], 0.0)
    
    def test_good_first_issue_detection(self):
        """Test good first issue label detection"""
        title = "Good first issue for beginners"
        body = "This is a simple task suitable for new contributors"
        
        result = self.handler.classify_issue(title, body)
        
        self.assertIn('good first issue', result['labels'])


class TestEmergencyThrottle(unittest.TestCase):
    """Test emergency issue throttling"""
    
    def setUp(self):
        """Set up test handler"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': '', 'DRY_RUN': 'true'}):
            self.handler = EnhancedIssueHandler()
    
    def test_throttle_check_no_repo(self):
        """Test throttle check without repo connection"""
        result = self.handler.check_emergency_throttle()
        self.assertTrue(result)  # Should allow by default in dry-run
    
    @patch('enhanced_issue_handler.Github')
    def test_throttle_check_with_many_emergencies(self, mock_github):
        """Test throttle activates with many emergency issues"""
        # Mock repository and issues
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.created_at = datetime.utcnow()
        mock_repo.get_issues.return_value = [mock_issue] * 5  # 5 emergency issues
        
        with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token', 'DRY_RUN': 'false'}):
            handler = EnhancedIssueHandler()
            handler.repo = mock_repo
            handler.dry_run = False
            
            result = handler.check_emergency_throttle()
            
            self.assertFalse(result)  # Should throttle


class TestDuplicateDetection(unittest.TestCase):
    """Test duplicate issue detection"""
    
    def setUp(self):
        """Set up test handler"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': '', 'DRY_RUN': 'true'}):
            self.handler = EnhancedIssueHandler()
    
    def test_find_similar_no_repo(self):
        """Test similarity check without repo"""
        result = self.handler.find_similar_issues("Test title", "Test body")
        self.assertEqual(result, [])
    
    @patch('enhanced_issue_handler.Github')
    def test_find_exact_duplicate(self, mock_github):
        """Test finding exact duplicate"""
        mock_repo = Mock()
        mock_issue = Mock()
        mock_issue.number = 123
        mock_issue.title = "Bug: Application crashes"
        mock_issue.body = "The app crashes on startup"
        mock_issue.html_url = "https://github.com/test/repo/issues/123"
        mock_repo.get_issues.return_value = [mock_issue]
        
        with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token', 'DRY_RUN': 'false'}):
            handler = EnhancedIssueHandler()
            handler.repo = mock_repo
            handler.dry_run = False
            
            similar = handler.find_similar_issues(
                "Bug: Application crashes",
                "The app crashes on startup"
            )
            
            self.assertGreater(len(similar), 0)
            self.assertGreater(similar[0]['similarity'], 0.7)


class TestResponseGeneration(unittest.TestCase):
    """Test auto-response generation"""
    
    def setUp(self):
        """Set up test handler"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': '', 'DRY_RUN': 'true'}):
            self.handler = EnhancedIssueHandler()
    
    def test_generate_security_response(self):
        """Test security issue response"""
        classification = {
            'category': 'security',
            'priority': 'critical',
            'confidence': 0.95
        }
        
        response = self.handler.generate_response(1, classification, [])
        
        self.assertIn('Security Issue Detected', response)
        self.assertIn('critical', response.lower())
        self.assertIn('HYPERAI Framework', response)
        self.assertIn('alpha_prime_omega', response)
    
    def test_generate_bug_response(self):
        """Test bug issue response"""
        classification = {
            'category': 'bug',
            'priority': 'high',
            'confidence': 0.85
        }
        
        response = self.handler.generate_response(2, classification, [])
        
        self.assertIn('Bug Report', response)
        self.assertIn('reproduce', response)
        self.assertIn('HYPERAI Framework', response)
    
    def test_generate_feature_response(self):
        """Test feature request response"""
        classification = {
            'category': 'feature',
            'priority': 'medium',
            'confidence': 0.75
        }
        
        response = self.handler.generate_response(3, classification, [])
        
        self.assertIn('Feature Request', response)
        self.assertIn('DAIOF', response)
        self.assertIn('alpha_prime_omega', response)
    
    def test_generate_response_with_duplicates(self):
        """Test response with similar issues"""
        classification = {
            'category': 'bug',
            'priority': 'high',
            'confidence': 0.8
        }
        
        similar = [
            {'number': 100, 'title': 'Similar bug', 'similarity': 0.85},
            {'number': 101, 'title': 'Another similar', 'similarity': 0.75}
        ]
        
        response = self.handler.generate_response(4, classification, similar)
        
        self.assertIn('Related Issues', response)
        self.assertIn('#100', response)
        self.assertIn('85%', response)


class TestHYPERAIAttribution(unittest.TestCase):
    """Test HYPERAI Framework attribution"""
    
    def setUp(self):
        """Set up test handler"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': '', 'DRY_RUN': 'true'}):
            self.handler = EnhancedIssueHandler()
    
    def test_attribution_in_responses(self):
        """Test all responses include proper attribution"""
        classification = {
            'category': 'general',
            'priority': 'medium',
            'confidence': 0.7
        }
        
        response = self.handler.generate_response(1, classification, [])
        
        # Check required attribution elements
        self.assertIn('HYPERAI Framework', response)
        self.assertIn('Nguyễn Đức Cường', response)
        self.assertIn('alpha_prime_omega', response)
        self.assertIn('October 30, 2025', response)


class TestFourPillarsCompliance(unittest.TestCase):
    """Test 4 Pillars compliance"""
    
    def setUp(self):
        """Set up test handler"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': '', 'DRY_RUN': 'true'}):
            self.handler = EnhancedIssueHandler()
    
    def test_safety_pillar(self):
        """Test Safety: All operations are reversible"""
        # Handler should work in dry-run mode
        self.assertTrue(self.handler.dry_run or not self.handler.repo)
        
        # Config should have safe defaults
        self.assertGreaterEqual(self.handler.config['emergency_throttle_hours'], 1)
    
    def test_longterm_pillar(self):
        """Test Long-term: Sustainable automation"""
        # Should auto-close stale issues
        self.assertGreaterEqual(self.handler.config['auto_close_days'], 7)
    
    def test_datadriven_pillar(self):
        """Test Data-driven: Uses metrics and patterns"""
        # Classification returns confidence scores
        result = self.handler.classify_issue("Test", "Test body")
        self.assertIn('confidence', result)
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)
    
    def test_risk_management_pillar(self):
        """Test Risk Management: Throttling and validation"""
        # Emergency throttling is configured
        self.assertIn('emergency_throttle_hours', self.handler.config)
        self.assertGreater(self.handler.config['emergency_throttle_hours'], 0)


def run_tests():
    """Run all tests and return result"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestIssueClassification))
    suite.addTests(loader.loadTestsFromTestCase(TestEmergencyThrottle))
    suite.addTests(loader.loadTestsFromTestCase(TestDuplicateDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestHYPERAIAttribution))
    suite.addTests(loader.loadTestsFromTestCase(TestFourPillarsCompliance))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    print("=" * 80)
    print("Testing Enhanced Issue Handler")
    print("Powered by HYPERAI Framework")
    print("Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    print("=" * 80)
    
    exit_code = run_tests()
    
    print("=" * 80)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print("=" * 80)
    
    sys.exit(exit_code)
