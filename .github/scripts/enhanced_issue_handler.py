#!/usr/bin/env python3
"""
Enhanced Automatic Git Issue Handler
Xử lý tự động các vấn đề trên tài khoản Git

Powered by HYPERAI Framework
Creator: Nguyễn Đức Cường (alpha_prime_omega)
Original Creation: October 30, 2025

Features:
- Intelligent issue classification
- Smart priority assignment
- Duplicate detection
- Auto-response with context
- Emergency issue throttling
- Pattern-based routing
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

try:
    from github import Github, GithubException
except ImportError:
    print("📦 Installing PyGithub...")
    os.system("pip install -q PyGithub")
    from github import Github, GithubException


class EnhancedIssueHandler:
    """
    Intelligent issue handler with HYPERAI Framework principles
    Follows 4 Pillars: Safety, Long-term, Data-driven, Risk Management
    """
    
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('GITHUB_REPOSITORY', 'NguyenCuong1989/DAIOF-Framework')
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        
        # Configuration
        self.config = {
            'emergency_throttle_hours': 6,  # Only one emergency issue per 6 hours
            'max_similar_threshold': 0.7,   # Similarity threshold for duplicates
            'auto_close_days': 30,           # Auto-close stale issues after 30 days
            'priority_keywords': {
                'critical': ['critical', 'urgent', 'security', 'vulnerability', 'crash', 'data loss'],
                'high': ['bug', 'error', 'broken', 'not working', 'failed'],
                'medium': ['enhancement', 'feature', 'improvement'],
                'low': ['documentation', 'typo', 'question', 'discussion']
            },
            'category_keywords': {
                'security': ['security', 'vulnerability', 'exploit', 'cve'],
                'bug': ['bug', 'error', 'crash', 'exception', 'traceback'],
                'feature': ['feature', 'enhancement', 'add', 'support'],
                'documentation': ['docs', 'documentation', 'readme', 'guide'],
                'performance': ['slow', 'performance', 'optimization', 'speed'],
                'question': ['question', 'how to', 'help', 'usage']
            }
        }
        
        # Initialize GitHub connection
        if not self.token:
            print("⚠️  GITHUB_TOKEN not set - running in DRY-RUN mode")
            self.gh = None
            self.repo = None
            self.dry_run = True
        else:
            try:
                self.gh = Github(self.token)
                self.repo = self.gh.get_repo(self.repo_name)
                print(f"✅ Connected to {self.repo_name}")
            except Exception as e:
                print(f"❌ GitHub connection failed: {e}")
                self.gh = None
                self.repo = None
                self.dry_run = True
    
    def log(self, message: str, level: str = "INFO"):
        """Log with timestamp and level"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def classify_issue(self, title: str, body: str) -> Dict[str, any]:
        """
        Classify issue using intelligent keyword analysis
        Returns: {category, priority, labels, confidence}
        """
        text = (title + " " + (body or "")).lower()
        
        # Detect category
        category_scores = defaultdict(int)
        for category, keywords in self.config['category_keywords'].items():
            for keyword in keywords:
                if keyword in text:
                    category_scores[category] += 1
        
        category = max(category_scores, key=category_scores.get) if category_scores else 'general'
        
        # Detect priority
        priority = 'low'
        for level in ['critical', 'high', 'medium', 'low']:
            for keyword in self.config['priority_keywords'][level]:
                if keyword in text:
                    priority = level
                    break
            if priority == level:
                break
        
        # Generate labels
        labels = [category]
        if priority in ['critical', 'high']:
            labels.append(f'priority: {priority}')
        
        # Add special labels
        if 'emergency' in text:
            labels.append('emergency')
        if 'good first issue' in text or 'beginner' in text:
            labels.append('good first issue')
        if 'help wanted' in text:
            labels.append('help wanted')
        
        labels.append('auto-classified')
        
        confidence = min(1.0, sum(category_scores.values()) / 3.0)
        
        return {
            'category': category,
            'priority': priority,
            'labels': labels,
            'confidence': confidence
        }
    
    def check_emergency_throttle(self) -> bool:
        """
        Check if we should create/allow emergency issues
        Returns: True if allowed, False if throttled
        """
        if not self.repo or self.dry_run:
            return True
        
        try:
            # Get recent emergency issues
            since = datetime.utcnow() - timedelta(hours=self.config['emergency_throttle_hours'])
            issues = self.repo.get_issues(
                state='all',
                labels=['emergency'],
                since=since
            )
            
            emergency_count = sum(1 for _ in issues)
            
            if emergency_count >= 3:  # Max 3 emergency issues in throttle window
                self.log(f"⚠️ Emergency throttle: {emergency_count} issues in last {self.config['emergency_throttle_hours']}h", "WARNING")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"Error checking emergency throttle: {e}", "ERROR")
            return True  # Allow by default on error
    
    def find_similar_issues(self, title: str, body: str, threshold: float = 0.7) -> List[Dict]:
        """
        Find similar/duplicate issues using text similarity
        Returns: List of similar issues with similarity scores
        """
        if not self.repo or self.dry_run:
            return []
        
        try:
            # Get open issues
            open_issues = self.repo.get_issues(state='open')
            similar = []
            
            query_text = (title + " " + (body or "")).lower()
            query_words = set(re.findall(r'\w+', query_text))
            
            for issue in open_issues[:50]:  # Check last 50 open issues
                issue_text = (issue.title + " " + (issue.body or "")).lower()
                issue_words = set(re.findall(r'\w+', issue_text))
                
                # Simple Jaccard similarity
                if query_words and issue_words:
                    similarity = len(query_words & issue_words) / len(query_words | issue_words)
                    
                    if similarity >= threshold:
                        similar.append({
                            'number': issue.number,
                            'title': issue.title,
                            'similarity': similarity,
                            'url': issue.html_url
                        })
            
            return sorted(similar, key=lambda x: x['similarity'], reverse=True)
            
        except Exception as e:
            self.log(f"Error finding similar issues: {e}", "ERROR")
            return []
    
    def generate_response(self, issue_number: int, classification: Dict, similar_issues: List[Dict]) -> str:
        """
        Generate intelligent auto-response based on issue classification
        """
        category = classification['category']
        priority = classification['priority']
        
        response = f"👋 **Thank you for opening this issue!**\n\n"
        response += f"🤖 The DAIOF Digital Organism has automatically analyzed this issue:\n\n"
        response += f"- **Category**: {category.capitalize()}\n"
        response += f"- **Priority**: {priority.capitalize()}\n"
        response += f"- **Confidence**: {classification['confidence']:.0%}\n\n"
        
        # Category-specific guidance
        if category == 'security':
            response += "🔒 **Security Issue Detected**\n"
            response += "This issue has been marked as high priority. Our security team will review it promptly.\n"
            response += "Please do NOT disclose exploit details publicly until patched.\n\n"
        
        elif category == 'bug':
            response += "🐛 **Bug Report**\n"
            response += "To help us fix this faster, please ensure you've provided:\n"
            response += "- Steps to reproduce\n"
            response += "- Expected vs actual behavior\n"
            response += "- Environment details (OS, Python version, DAIOF version)\n"
            response += "- Error messages or logs\n\n"
        
        elif category == 'feature':
            response += "✨ **Feature Request**\n"
            response += "Thank you for helping DAIOF evolve! Consider:\n"
            response += "- How this aligns with DAIOF's biological philosophy\n"
            response += "- Impact on AI-Human interdependence\n"
            response += "- Implementation complexity\n\n"
        
        elif category == 'question':
            response += "❓ **Question/Help**\n"
            response += "For faster answers, check:\n"
            response += "- [Documentation](https://github.com/NguyenCuong1989/DAIOF-Framework#readme)\n"
            response += "- [Examples](https://github.com/NguyenCuong1989/DAIOF-Framework/tree/main/examples)\n"
            response += "- [Discussions](https://github.com/NguyenCuong1989/DAIOF-Framework/discussions)\n\n"
        
        # Similar issues warning
        if similar_issues:
            response += "⚠️ **Possibly Related Issues:**\n"
            for sim in similar_issues[:3]:  # Show top 3
                response += f"- #{sim['number']}: {sim['title']} ({sim['similarity']:.0%} similar)\n"
            response += "\nPlease check if these address your concern.\n\n"
        
        # Footer
        response += "---\n"
        response += "*🤖 Automated by DAIOF Digital Organism*\n"
        response += "*Powered by HYPERAI Framework | Creator: Nguyễn Đức Cường (alpha_prime_omega)*\n"
        response += "*Original Creation: October 30, 2025*"
        
        return response
    
    def process_new_issue(self, issue_number: int):
        """
        Main processing logic for new issues
        Applies 4 Pillars principles
        """
        if not self.repo:
            self.log("Cannot process issue without repo connection", "ERROR")
            return
        
        try:
            issue = self.repo.get_issue(issue_number)
            self.log(f"Processing issue #{issue_number}: {issue.title}")
            
            # Safety check: Don't process if already labeled
            existing_labels = [label.name for label in issue.labels]
            if 'auto-classified' in existing_labels:
                self.log(f"Issue #{issue_number} already processed", "INFO")
                return
            
            # Emergency throttle check
            if 'emergency' in issue.title.lower() or 'emergency' in (issue.body or "").lower():
                if not self.check_emergency_throttle():
                    self.log(f"Emergency issue #{issue_number} throttled", "WARNING")
                    
                    if not self.dry_run:
                        issue.create_comment(
                            "⚠️ **Emergency Issue Throttle**\n\n"
                            "Multiple emergency issues detected recently. This issue has been throttled.\n"
                            "If this is a genuine emergency, please add more details and ping @NguyenCuong1989.\n\n"
                            "*Automated throttle by DAIOF Digital Organism*"
                        )
                        issue.edit(labels=['emergency', 'throttled'])
                    return
            
            # Classify issue
            classification = self.classify_issue(issue.title, issue.body or "")
            self.log(f"Classification: {classification}")
            
            # Find duplicates
            similar_issues = self.find_similar_issues(
                issue.title, 
                issue.body or "", 
                self.config['max_similar_threshold']
            )
            
            if similar_issues:
                self.log(f"Found {len(similar_issues)} similar issues")
            
            # Apply labels
            if not self.dry_run:
                try:
                    issue.edit(labels=classification['labels'])
                    self.log(f"Applied labels: {classification['labels']}")
                except Exception as e:
                    self.log(f"Error applying labels: {e}", "ERROR")
            
            # Generate and post response
            response = self.generate_response(issue_number, classification, similar_issues)
            
            if not self.dry_run:
                try:
                    issue.create_comment(response)
                    self.log(f"Posted auto-response to #{issue_number}")
                except Exception as e:
                    self.log(f"Error posting comment: {e}", "ERROR")
            else:
                self.log("DRY-RUN: Would post response:", "DEBUG")
                print(response)
            
            # Auto-close obvious duplicates
            if similar_issues and similar_issues[0]['similarity'] > 0.9:
                self.log(f"High similarity ({similar_issues[0]['similarity']:.0%}) with #{similar_issues[0]['number']}", "WARNING")
                
                if not self.dry_run and classification['confidence'] > 0.8:
                    dup_comment = (
                        f"🔄 **Possible Duplicate**\n\n"
                        f"This appears to be very similar to #{similar_issues[0]['number']}.\n"
                        f"If this is not a duplicate, please provide additional details that distinguish it.\n\n"
                        f"Marking as potential duplicate for review."
                    )
                    issue.create_comment(dup_comment)
                    issue.add_to_labels('duplicate')
            
            self.log(f"✅ Successfully processed issue #{issue_number}")
            
        except Exception as e:
            self.log(f"Error processing issue #{issue_number}: {e}", "ERROR")
            raise
    
    def process_all_open_issues(self):
        """
        Process all open issues that haven't been auto-classified
        """
        if not self.repo:
            self.log("Cannot process issues without repo connection", "ERROR")
            return
        
        try:
            open_issues = self.repo.get_issues(state='open')
            processed = 0
            skipped = 0
            
            for issue in open_issues:
                # Skip pull requests
                if issue.pull_request:
                    continue
                
                # Skip if already processed
                labels = [label.name for label in issue.labels]
                if 'auto-classified' in labels:
                    skipped += 1
                    continue
                
                self.process_new_issue(issue.number)
                processed += 1
            
            self.log(f"Batch processing complete: {processed} processed, {skipped} skipped")
            
        except Exception as e:
            self.log(f"Error in batch processing: {e}", "ERROR")


def main():
    """Main entry point"""
    print("=" * 80)
    print("🤖 Enhanced Git Issue Handler")
    print("Powered by HYPERAI Framework")
    print("Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    print("=" * 80)
    
    handler = EnhancedIssueHandler()
    
    # Get issue number from environment or process all
    issue_number = os.getenv('ISSUE_NUMBER')
    
    if issue_number:
        # Process specific issue
        try:
            issue_num = int(issue_number)
            handler.process_new_issue(issue_num)
        except ValueError:
            print(f"❌ Invalid issue number: {issue_number}")
            sys.exit(1)
    else:
        # Process all open issues
        handler.process_all_open_issues()
    
    print("=" * 80)
    print("✅ Issue processing complete")
    print("=" * 80)


if __name__ == "__main__":
    main()
