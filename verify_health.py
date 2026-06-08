#!/usr/bin/env python3
"""
Ecosystem Health Verifier
========================

Comprehensive health check for DAIOF Framework

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Verification: 4287
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class HealthChecker:
    """Comprehensive health checker for the ecosystem"""
    
    def __init__(self):
        self.passed_checks = 0
        self.failed_checks = 0
        self.warnings = []
        self.issues = []
    
    def check_module_structure(self):
        """Check if module structure is complete"""
        print("📦 Checking module structure...")
        
        required_modules = [
            "src/hyperai/__init__.py",
            "src/hyperai/core/haios_core.py",
            "src/hyperai/core/haios_runtime.py",
            "src/hyperai/components/genome.py",
            "src/hyperai/components/metabolism.py",
            "src/hyperai/components/nervous_system.py",
            "src/hyperai/components/organism.py",
            "src/hyperai/ecosystem/ecosystem.py",
            "src/hyperai/protocols/symphony.py",
            "src/hyperai/protocols/dr_protocol.py",
            "src/hyperai/protocols/metadata.py",
        ]
        
        missing = []
        for module in required_modules:
            if not (project_root / module).exists():
                missing.append(module)
        
        if missing:
            self.failed_checks += 1
            self.issues.append(f"Missing modules: {', '.join(missing)}")
            print(f"  ❌ Missing {len(missing)} modules")
        else:
            self.passed_checks += 1
            print(f"  ✅ All {len(required_modules)} required modules present")
    
    def check_imports(self):
        """Check if imports work correctly"""
        print("\n📥 Checking imports...")
        
        try:
            from src.hyperai import (
                HAIOSCore,
                DigitalOrganism,
                DigitalEcosystem,
                SymphonyControlCenter
            )
            self.passed_checks += 1
            print("  ✅ All core imports successful")
        except ImportError as e:
            self.failed_checks += 1
            self.issues.append(f"Import error: {e}")
            print(f"  ❌ Import failed: {e}")
    
    def check_tests(self):
        """Check if tests exist and are runnable"""
        print("\n🧪 Checking tests...")
        
        test_files = list((project_root / "tests").glob("test_*.py"))
        
        if len(test_files) < 2:
            self.warnings.append(f"Only {len(test_files)} test files found (expected 2+)")
            print(f"  ⚠️  Only {len(test_files)} test files")
        else:
            self.passed_checks += 1
            print(f"  ✅ Found {len(test_files)} test files")
        
        # Try running tests
        import subprocess
        try:
            result = subprocess.run(
                [sys.executable, "tests/test_smoke.py"],
                cwd=project_root,
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                self.passed_checks += 1
                print("  ✅ Smoke tests pass")
            else:
                self.failed_checks += 1
                self.issues.append("Smoke tests failed")
                print("  ❌ Smoke tests failed")
        except Exception as e:
            self.warnings.append(f"Could not run tests: {e}")
            print(f"  ⚠️  Could not run tests: {e}")
    
    def check_documentation(self):
        """Check documentation completeness"""
        print("\n📚 Checking documentation...")
        
        required_docs = [
            "README.md",
            "LICENSE",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
        ]
        
        missing_docs = []
        for doc in required_docs:
            if not (project_root / doc).exists():
                missing_docs.append(doc)
        
        if missing_docs:
            self.warnings.append(f"Missing docs: {', '.join(missing_docs)}")
            print(f"  ⚠️  Missing {len(missing_docs)} documentation files")
        else:
            self.passed_checks += 1
            print(f"  ✅ All {len(required_docs)} required docs present")
    
    def check_package_structure(self):
        """Check if package can be built"""
        print("\n📦 Checking package structure...")
        
        required_files = [
            "setup.py",
            "requirements.txt",
            "MANIFEST.in",
        ]
        
        missing = []
        for file in required_files:
            if not (project_root / file).exists():
                missing.append(file)
        
        if missing:
            self.warnings.append(f"Missing package files: {', '.join(missing)}")
            print(f"  ⚠️  Missing {len(missing)} package files")
        else:
            self.passed_checks += 1
            print(f"  ✅ All package files present")
    
    def check_git_health(self):
        """Check Git repository health"""
        print("\n🔧 Checking Git health...")
        
        import subprocess
        try:
            # Check if in git repo
            result = subprocess.run(
                ["git", "status"],
                cwd=project_root,
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                self.passed_checks += 1
                print("  ✅ Git repository healthy")
            else:
                self.warnings.append("Git status check failed")
                print("  ⚠️  Git status issues")
        except Exception as e:
            self.warnings.append(f"Git check failed: {e}")
            print(f"  ⚠️  Could not check Git: {e}")
    
    def generate_report(self):
        """Generate final health report"""
        print("\n" + "="*60)
        print("🏥 ECOSYSTEM HEALTH REPORT")
        print("="*60)
        
        total_checks = self.passed_checks + self.failed_checks
        if total_checks > 0:
            health_percentage = (self.passed_checks / total_checks) * 100
        else:
            health_percentage = 0
        
        print(f"\n📊 Results:")
        print(f"  ✅ Passed: {self.passed_checks}")
        print(f"  ❌ Failed: {self.failed_checks}")
        print(f"  ⚠️  Warnings: {len(self.warnings)}")
        print(f"\n💚 Health Score: {health_percentage:.1f}%")
        
        if self.issues:
            print(f"\n🚨 Critical Issues ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  • {issue}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        print("\n" + "="*60)
        
        if health_percentage >= 80:
            print("✅ ECOSYSTEM HEALTHY")
            return 0
        elif health_percentage >= 60:
            print("⚠️  ECOSYSTEM NEEDS ATTENTION")
            return 1
        else:
            print("🚨 ECOSYSTEM CRITICAL")
            return 2


def main():
    """Run comprehensive health check"""
    print("🧬 DAIOF Framework - Ecosystem Health Check")
    print("=" * 60)
    print("Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    print("Verification: 4287")
    print("=" * 60 + "\n")
    
    checker = HealthChecker()
    
    # Run all checks
    checker.check_module_structure()
    checker.check_imports()
    checker.check_tests()
    checker.check_documentation()
    checker.check_package_structure()
    checker.check_git_health()
    
    # Generate report
    exit_code = checker.generate_report()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
