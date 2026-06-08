#!/usr/bin/env python3
"""
Validate GitHub issue templates.

This script validates the YAML syntax and structure of GitHub issue templates
to ensure they conform to GitHub's form schema.

Usage:
    python .github/scripts/validate_issue_templates.py
"""

import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any


def validate_yaml_syntax(file_path: Path) -> bool:
    """Validate YAML syntax."""
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        print(f"✅ {file_path.name}: Valid YAML syntax")
        return True
    except yaml.YAMLError as e:
        print(f"❌ {file_path.name}: Invalid YAML syntax - {e}")
        return False


def validate_issue_form_structure(file_path: Path) -> bool:
    """Validate GitHub issue form structure."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check required top-level fields
        if 'name' not in data:
            print(f"❌ {file_path.name}: Missing required field 'name'")
            return False
        
        if 'description' not in data:
            print(f"❌ {file_path.name}: Missing required field 'description'")
            return False
        
        if 'body' not in data:
            print(f"❌ {file_path.name}: Missing required field 'body'")
            return False
        
        if not isinstance(data['body'], list):
            print(f"❌ {file_path.name}: 'body' must be a list")
            return False
        
        # Validate body items
        valid_types = ['markdown', 'textarea', 'input', 'dropdown', 'checkboxes']
        for idx, item in enumerate(data['body']):
            if 'type' not in item:
                print(f"❌ {file_path.name}: Body item {idx} missing 'type'")
                return False
            
            if item['type'] not in valid_types:
                print(f"❌ {file_path.name}: Body item {idx} has invalid type '{item['type']}'")
                return False
            
            if 'attributes' not in item:
                print(f"❌ {file_path.name}: Body item {idx} missing 'attributes'")
                return False
        
        print(f"✅ {file_path.name}: Valid issue form structure")
        return True
    
    except Exception as e:
        print(f"❌ {file_path.name}: Validation error - {e}")
        return False


def validate_config_structure(file_path: Path) -> bool:
    """Validate config.yml structure."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if 'blank_issues_enabled' not in data:
            print(f"⚠️  {file_path.name}: 'blank_issues_enabled' not set (optional)")
        
        if 'contact_links' in data:
            if not isinstance(data['contact_links'], list):
                print(f"❌ {file_path.name}: 'contact_links' must be a list")
                return False
            
            for idx, link in enumerate(data['contact_links']):
                required = ['name', 'url', 'about']
                for field in required:
                    if field not in link:
                        print(f"❌ {file_path.name}: Contact link {idx} missing '{field}'")
                        return False
        
        print(f"✅ {file_path.name}: Valid config structure")
        return True
    
    except Exception as e:
        print(f"❌ {file_path.name}: Validation error - {e}")
        return False


def main():
    """Main validation function."""
    print("🔍 Validating GitHub Issue Templates\n")
    
    # Get template directory
    repo_root = Path(__file__).parent.parent.parent
    template_dir = repo_root / ".github" / "ISSUE_TEMPLATE"
    
    if not template_dir.exists():
        print(f"❌ Template directory not found: {template_dir}")
        return 1
    
    all_valid = True
    
    # Validate config.yml
    config_file = template_dir / "config.yml"
    if config_file.exists():
        print("📝 Validating config.yml")
        if not validate_yaml_syntax(config_file):
            all_valid = False
        elif not validate_config_structure(config_file):
            all_valid = False
        print()
    
    # Validate issue form templates
    form_templates = list(template_dir.glob("*.yml"))
    form_templates = [f for f in form_templates if f.name != "config.yml"]
    
    if form_templates:
        print(f"📝 Validating {len(form_templates)} issue form template(s)")
        for template in sorted(form_templates):
            if not validate_yaml_syntax(template):
                all_valid = False
            elif not validate_issue_form_structure(template):
                all_valid = False
        print()
    
    # Summary
    if all_valid:
        print("✅ All templates are valid!")
        return 0
    else:
        print("❌ Some templates have errors. Please fix them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
