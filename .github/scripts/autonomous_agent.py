#!/usr/bin/env python3
"""
AI Agent Autonomous Operations Script
Cho phép AI hoạt động độc lập trên GitHub thông qua GitHub Actions

Tuân thủ 4 Pillars:
- An toàn: Chỉ thực hiện các thay đổi an toàn, có thể revert
- Đường dài: Tập trung vào giá trị lâu dài, không spam
- Tin vào số liệu: Ra quyết định dựa trên metrics
- Hạn chế rủi ro con người: Tự động hóa nhưng có giới hạn rõ ràng
"""

import os
import sys
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

try:
    from github import Github, GithubException
except ImportError:
    print("❌ PyGithub not installed. Installing...")
    os.system("pip install PyGithub")
    from github import Github, GithubException


class AutonomousAIAgent:
    """AI Agent có khả năng hoạt động tự động trên GitHub"""
    
    def __init__(self):
        self.log = []  # Initialize log first
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('REPO_NAME', 'Copilot-home/DAIOF-Framework')
        self.task_type = os.getenv('TASK_TYPE', 'auto_maintain')
        self.dry_run = os.getenv('DRY_RUN', 'true').lower() == 'true'
        
        # If GITHUB_TOKEN not set, run in dry-run/local mode
        if not self.token:
            self.log_action("⚠️  GITHUB_TOKEN not set - running in LOCAL DRY-RUN MODE", "WARNING")
            self.gh = None
            self.repo = None
            self.dry_run = True
        else:
            try:
                self.gh = Github(self.token)
                self.repo = self.gh.get_repo(self.repo_name)
            except Exception as e:
                self.log_action(f"❌ GitHub connection failed: {e}", "ERROR")
                self.gh = None
                self.repo = None
                self.dry_run = True
        
    def log_action(self, message: str, level: str = "INFO"):
        """Ghi log các hành động của AI"""
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log.append(log_entry)
        print(log_entry)
        
    def get_repo_metrics(self):
        """Lấy metrics repo - return dummy values in dry-run mode"""
        if not self.repo:
            self.log_action("📊 Repository metrics unavailable: GitHub repository is not connected", "WARNING")
            return {
                'stars': None,
                'forks': None,
                'watchers': None,
                'open_issues': None,
                'subscribers': None,
            }

        if self.dry_run:
            self.log_action("📊 Dry-run: Reading repository metrics without mutation", "DEBUG")
        
        return {
            'stars': self.repo.stargazers_count,
            'forks': self.repo.forks_count,
            'watchers': self.repo.watchers_count,
            'open_issues': self.repo.open_issues_count,
            'subscribers': self.repo.subscribers_count,
        }
    
    def auto_maintain(self):
        """Tự động bảo trì repository"""
        self.log_action("🔧 Starting automatic maintenance...")
        
        # 1. Kiểm tra và update README badges
        self._update_readme_badges()
        
        # 2. Tạo daily metrics report
        self._create_metrics_report()
        
        # 3. Auto-label issues nếu có
        self._auto_label_issues()
        
        self.log_action("✅ Automatic maintenance completed")
    
    def _update_readme_badges(self):
        """Cập nhật badges trong README với metrics mới nhất"""
        if not self.repo or self.dry_run:
            self.log_action("📝 Dry-run: Skipping README badge update", "DEBUG")
            return
        
        try:
            readme = self.repo.get_contents("README.md")
            content = readme.decoded_content.decode('utf-8')
            
            metrics = self.get_repo_metrics()
            
            # Kiểm tra xem cần update không (chỉ update nếu metrics thay đổi đáng kể)
            # An toàn: Không spam commits không cần thiết
            self.log_action(f"📊 Current metrics: {metrics}")
            
        except Exception as e:
            self.log_action(f"⚠️ Badge update skipped: {str(e)}", "WARNING")
    
    def _create_metrics_report(self):
        """Tạo báo cáo metrics hàng ngày"""
        metrics = self.get_repo_metrics()
        timestamp = datetime.utcnow().strftime('%Y-%m-%d')
        
        report_dir = Path('metrics')
        report_dir.mkdir(exist_ok=True)
        
        report_file = report_dir / f'daily_{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump({
                'date': timestamp,
                'metrics': metrics,
                'timestamp': datetime.utcnow().isoformat()
            }, f, indent=2)
        
        self.log_action(f"📈 Metrics report created: {report_file}")
    
    def _auto_label_issues(self):
        """Tự động gắn labels cho issues mới"""
        if not self.repo or self.dry_run:
            self.log_action("🏷️ Dry-run: Skipping auto-labeling", "DEBUG")
            return
        
        try:
            # Lấy issues mở trong 24h qua chưa có label
            since = datetime.utcnow() - timedelta(days=1)
            issues = self.repo.get_issues(state='open', since=since)
            
            labeled_count = 0
            for issue in issues:
                if len(list(issue.labels)) == 0:
                    # AI phân tích nội dung và gắn label phù hợp
                    labels = self._suggest_labels(issue)
                    if labels:
                        issue.add_to_labels(*labels)
                        labeled_count += 1
                        self.log_action(f"🏷️ Auto-labeled issue #{issue.number}: {labels}")
            
            if labeled_count > 0:
                self.log_action(f"✅ Auto-labeled {labeled_count} issues")
            else:
                self.log_action("ℹ️ No issues need auto-labeling")
                
        except Exception as e:
            self.log_action(f"⚠️ Auto-labeling skipped: {str(e)}", "WARNING")
    
    def _suggest_labels(self, issue) -> List[str]:
        """AI phân tích issue và đề xuất labels phù hợp"""
        labels = []
        title_lower = issue.title.lower()
        body_lower = (issue.body or '').lower()
        
        # Simple keyword-based labeling (có thể nâng cấp với AI model sau)
        if any(word in title_lower for word in ['bug', 'error', 'fix', 'broken']):
            labels.append('bug')
        
        if any(word in title_lower for word in ['feature', 'enhancement', 'add']):
            labels.append('enhancement')
        
        if any(word in title_lower for word in ['doc', 'documentation', 'readme']):
            labels.append('documentation')
        
        if any(word in title_lower for word in ['question', 'help', 'how']):
            labels.append('question')
        
        return labels
    
    def community_engagement(self):
        """Tương tác với community một cách tự động"""
        self.log_action("👥 Starting community engagement...")
        
        # 1. Welcome new contributors
        self._welcome_new_contributors()
        
        # 2. Thank first-time contributors
        self._thank_contributors()
        
        # 3. Respond to questions (nếu có template)
        self._auto_respond_questions()
        
        self.log_action("✅ Community engagement completed")
    
    def _welcome_new_contributors(self):
        """Chào mừng contributors mới"""
        try:
            # Lấy PRs mở trong 24h qua
            since = datetime.utcnow() - timedelta(days=1)
            pulls = self.repo.get_pulls(state='open', sort='created')
            
            welcomed_count = 0
            for pr in pulls[:5]:  # Giới hạn 5 PRs gần nhất
                # Kiểm tra xem đây có phải first-time contributor không
                author_prs = list(self.repo.get_pulls(state='all', creator=pr.user.login))
                
                if len(author_prs) == 1:  # First PR from this user
                    # Kiểm tra xem đã welcome chưa
                    comments = list(pr.get_issue_comments())
                    already_welcomed = any('AI Agent 🤖' in c.body for c in comments)
                    
                    if not already_welcomed:
                        welcome_msg = f"""
🎉 **Welcome to DAIOF Framework, @{pr.user.login}!**

Thank you for your first contribution! 

The AI Agent has noticed your PR and will help guide it through the review process. A human maintainer will review your changes soon.

**Quick tips:**
- Make sure all tests pass ✅
- Follow our [Contributing Guidelines](../CONTRIBUTING.md)
- Feel free to ask questions!

---
*This is an automated message from the AI Agent 🤖*
"""
                        pr.create_issue_comment(welcome_msg)
                        welcomed_count += 1
                        self.log_action(f"👋 Welcomed first-time contributor: @{pr.user.login}")
            
            if welcomed_count > 0:
                self.log_action(f"✅ Welcomed {welcomed_count} new contributors")
            else:
                self.log_action("ℹ️ No new contributors to welcome")
                
        except Exception as e:
            self.log_action(f"⚠️ Welcome message skipped: {str(e)}", "WARNING")
    
    def _thank_contributors(self):
        """Cảm ơn contributors khi PR được merge"""
        try:
            # Lấy PRs merged trong 24h qua
            since = datetime.utcnow() - timedelta(days=1)
            pulls = self.repo.get_pulls(state='closed', sort='updated')
            
            thanked_count = 0
            for pr in pulls[:10]:  # Giới hạn 10 PRs
                if pr.merged and pr.merged_at and pr.merged_at > since:
                    # Kiểm tra xem đã thank chưa
                    comments = list(pr.get_issue_comments())
                    already_thanked = any('Thank you for your contribution' in c.body for c in comments)
                    
                    if not already_thanked:
                        thank_msg = f"""
🙏 **Thank you for your contribution, @{pr.user.login}!**

Your PR has been merged and is now part of DAIOF Framework. We appreciate your time and effort in making this project better!

⭐ If you enjoyed contributing, please consider starring the repo and sharing it with others!

---
*This is an automated message from the AI Agent 🤖*
"""
                        pr.create_issue_comment(thank_msg)
                        thanked_count += 1
                        self.log_action(f"🙏 Thanked contributor: @{pr.user.login}")
            
            if thanked_count > 0:
                self.log_action(f"✅ Thanked {thanked_count} contributors")
            else:
                self.log_action("ℹ️ No merged PRs to thank")
                
        except Exception as e:
            self.log_action(f"⚠️ Thank message skipped: {str(e)}", "WARNING")
    
    def _auto_respond_questions(self):
        """Tự động trả lời các câu hỏi thường gặp"""
        # An toàn: Chỉ respond với template có sẵn, không tự generate
        self.log_action("ℹ️ Auto-response to questions: Not implemented yet (safety)")
    
    def content_update(self):
        """Tự động cập nhật nội dung"""
        self.log_action("📝 Starting content update...")
        
        # 1. Update contributor list
        self._update_contributors()
        
        # 2. Generate changelog từ commits
        self._update_changelog()
        
        self.log_action("✅ Content update completed")
    
    def _update_contributors(self):
        """Cập nhật danh sách contributors"""
        try:
            contributors = self.repo.get_contributors()
            
            contrib_file = Path('CONTRIBUTORS.md')
            
            with open(contrib_file, 'w') as f:
                f.write("# Contributors\n\n")
                f.write("Thank you to all the amazing people who have contributed to DAIOF Framework!\n\n")
                
                for contrib in contributors:
                    contributions = contrib.contributions
                    f.write(f"- [@{contrib.login}]({contrib.html_url}) - {contributions} commits\n")
                
                f.write(f"\n---\n*Last updated: {datetime.utcnow().strftime('%Y-%m-%d')} by AI Agent 🤖*\n")
            
            self.log_action(f"👥 Updated contributors list")
            
        except Exception as e:
            self.log_action(f"⚠️ Contributors update skipped: {str(e)}", "WARNING")
    
    def _update_changelog(self):
        """Tự động generate changelog từ commits gần đây"""
        self.log_action("ℹ️ Changelog generation: Skipped (will be done manually)")
    
    def metrics_report(self):
        """Tạo báo cáo chi tiết về metrics"""
        self.log_action("📊 Generating detailed metrics report...")
        
        metrics = self.get_repo_metrics()
        
        report = f"""# Repository Metrics Report
Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Overview
- ⭐ Stars: {metrics['stars']}
- 🍴 Forks: {metrics['forks']}
- 👀 Watchers: {metrics['watchers']}
- 📝 Open Issues: {metrics['open_issues']}
- 👥 Subscribers: {metrics['subscribers']}

## Growth Analysis
*Analysis will be added when we have historical data*

---
*Generated by AI Agent 🤖*
"""
        
        report_file = Path('metrics') / f'report_{datetime.utcnow().strftime("%Y%m%d")}.md'
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            f.write(report)
        
        self.log_action(f"📊 Metrics report saved: {report_file}")
    
    def run(self):
        """Thực thi autonomous agent theo task type"""
        self.log_action(f"🚀 AI Agent starting: Task={self.task_type}")
        
        try:
            if self.task_type == 'auto_maintain':
                self.auto_maintain()
            elif self.task_type == 'community_engagement':
                self.community_engagement()
            elif self.task_type == 'content_update':
                self.content_update()
            elif self.task_type == 'metrics_report':
                self.metrics_report()
            else:
                self.log_action(f"⚠️ Unknown task type: {self.task_type}", "WARNING")
            
            self.log_action("✅ AI Agent completed successfully")
            
        except Exception as e:
            self.log_action(f"❌ AI Agent failed: {str(e)}", "ERROR")
            raise
        
        finally:
            # Save log
            log_file = Path('metrics') / f'agent_log_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.txt'
            log_file.parent.mkdir(exist_ok=True)
            
            with open(log_file, 'w') as f:
                f.write('\n'.join(self.log))
            
            print(f"\n📝 Log saved: {log_file}")


if __name__ == '__main__':
    agent = AutonomousAIAgent()
    agent.run()
