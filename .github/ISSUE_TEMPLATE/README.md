# Issue Templates

This directory contains GitHub issue templates for the DAIOF Framework.

## Template Types

### YAML Templates (Recommended) ✅
- `bug_report.yml` - Report bugs with structured form
- `feature_request.yml` - Request new features
- `documentation.yml` - Suggest documentation improvements
- `question.yml` - Ask questions

**Benefits:**
- ✅ Required field validation
- ✅ Structured input (dropdowns, checkboxes)
- ✅ Prevents empty submissions
- ✅ Better user experience

### Markdown Templates (Legacy)
- `bug_report.md`
- `feature_request.md`
- `documentation.md`
- `question.md`

**Note:** Markdown templates are kept for backward compatibility but YAML templates are preferred.

## Configuration

- `config.yml` - Configures issue template chooser
  - Disables blank issues
  - Adds helpful resource links
  - Directs users to appropriate channels

## Usage Guide

See [ISSUE_TEMPLATE_GUIDE.md](../ISSUE_TEMPLATE_GUIDE.md) for:
- How to choose the right template
- Writing quality issues
- Best practices
- Common mistakes to avoid

## For Maintainers

### Testing Templates Locally

Validate YAML syntax:
```bash
cd .github/ISSUE_TEMPLATE
yamllint -c .yamllint *.yml
```

Check Python parsing:
```bash
python3 -c "import yaml; yaml.safe_load(open('config.yml'))"
```

### Modifying Templates

1. Edit the `.yml` files
2. Validate syntax
3. Test on GitHub (create test issue)
4. Update corresponding `.md` file if needed
5. Update ISSUE_TEMPLATE_GUIDE.md

### GitHub Issue Form Schema

Reference: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema

Supported input types:
- `markdown` - Display text
- `textarea` - Multi-line text input
- `input` - Single-line text input
- `dropdown` - Select from options
- `checkboxes` - Multiple selections

---

**Attribution:** Powered by HYPERAI Framework  
**Creator:** Nguyễn Đức Cường (alpha_prime_omega)  
**Framework Created:** October 30, 2025
