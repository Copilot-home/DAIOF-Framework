# 📝 Issue Template Guide

## Overview

DAIOF uses structured issue templates to ensure high-quality bug reports, feature requests, and questions. This guide helps you understand how to use them effectively.

## 🎯 Choosing the Right Template

### 🐛 Bug Report
**Use when:**
- Something is broken or not working as expected
- You've found an error or crash
- The framework behaves differently than documented

**Example:** "DigitalOrganism.evolve() crashes with negative generations"

### 🚀 Feature Request
**Use when:**
- You want to propose a new feature
- You have an idea for improvement
- You want to extend DAIOF's capabilities

**Example:** "Add Symphony Dashboard for multi-organism monitoring"

### 📖 Documentation
**Use when:**
- Documentation is missing, unclear, or wrong
- Examples need improvement
- API documentation is incomplete

**Example:** "Missing documentation for selection_pressure parameter"

### ❓ Question
**Use when:**
- You need help understanding DAIOF concepts
- You're stuck implementing something
- You need architectural guidance

**Example:** "How to implement custom selection strategies?"

**Note:** For general discussions, use [GitHub Discussions](https://github.com/NguyenCuong1989/DAIOF-Framework/discussions) instead.

## ✅ Writing Quality Issues

### 1. Search First
Before creating an issue:
- Search existing issues: `is:issue your-search-term`
- Check [closed issues](https://github.com/NguyenCuong1989/DAIOF-Framework/issues?q=is%3Aissue+is%3Aclosed): `is:closed your-search-term`
- Browse [discussions](https://github.com/NguyenCuong1989/DAIOF-Framework/discussions)

### 2. Provide Complete Information
All required fields (marked with *) must be filled. The better your description, the faster we can help.

### 3. Include Code Samples
For bugs and questions, always include:
```python
# Minimal reproducible example
from digital_ai_organism_framework import DigitalOrganism

organism = DigitalOrganism()
# Your code that demonstrates the issue
```

### 4. Specify Versions
Always include:
- DAIOF version: `pip show digital-ai-organism-framework`
- Python version: `python --version`
- Operating system: `macOS 14.0`, `Ubuntu 22.04`, etc.

### 5. Respect IP Guidelines
Before contributing features, review:
- [Contributing Guide](../CONTRIBUTING.md)
- [IP Classification](../INTELLECTUAL_PROPERTY_CLASSIFICATION.md)

## 🎯 Feature Request Best Practices

### Good Feature Request ✅
```markdown
**Problem:** When monitoring 10+ organisms, I need to switch between 
terminal windows to see their status.

**Solution:** Add a SymphonyDashboard that displays real-time metrics 
for all organisms in a web interface.

**Implementation:**
- Use Flask for web server
- WebSocket for real-time updates
- Aggregate metrics from MetricsCollector

**Benefits:** 
- Saves time for researchers
- Professional monitoring capability
- Aligns with Symphony metaphor

**Drawbacks:**
- Adds Flask dependency
- Requires port configuration
```

### Poor Feature Request ❌
```markdown
**Problem:** Add dashboard

**Solution:** Make UI

(Too vague, no details, can't implement)
```

## 🐛 Bug Report Best Practices

### Good Bug Report ✅
```markdown
**Description:** evolve() crashes when generations is negative

**Steps:**
1. Install DAIOF 1.0.0
2. Create organism: organism = DigitalOrganism()
3. Call: organism.evolve(generations=-5)
4. Crash occurs

**Expected:** Should raise ValueError
**Actual:** Unhandled TypeError

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.11.5
- DAIOF: 1.0.0

**Code:**
```python
organism = DigitalOrganism()
organism.evolve(generations=-5)  # Crashes here
```

**Error:**
```
TypeError: 'int' object is not iterable
  at digital_ai_organism_framework.py:234
```
```

### Poor Bug Report ❌
```markdown
**Description:** It doesn't work

**Steps:** I tried to use it

(No details, can't reproduce, can't fix)
```

## 🎼 Alignment with DAIOF Philosophy

When proposing features, consider:

### ✅ Good Alignment
- **Biological metaphors**: "Add organism migration between environments"
- **AI-Human interdependence**: "Require human approval for risky mutations"
- **Safety-first**: "Add rollback mechanism for failed evolutions"
- **Consciousness development**: "Track decision-making patterns over time"

### ❌ Poor Alignment
- "Remove creator attribution" (Violates immutable genes)
- "Allow organisms to self-modify core genes" (Violates safety)
- "Make humans optional" (Violates interdependence)

## 📊 Template Field Explanations

### Feature Request Fields

| Field | Purpose | Example |
|-------|---------|---------|
| **Problem Statement** | What frustration/gap does this solve? | "Can't monitor multiple organisms" |
| **Proposed Solution** | What should happen? | "Add Symphony Dashboard" |
| **Implementation Ideas** | Technical approach (optional) | "Use Flask + WebSocket" |
| **Alternatives** | What else did you consider? | "Use Grafana, manual logging" |
| **Philosophy Alignment** | How does it fit DAIOF? | Check biological metaphors |
| **Benefits** | Who wins? | "Researchers, enterprises" |
| **Drawbacks** | What are the costs? | "Memory overhead, complexity" |
| **Usage Example** | How would it work? | Code showing usage |

### Bug Report Fields

| Field | Purpose | Example |
|-------|---------|---------|
| **Description** | What's wrong? | "Crash on negative generations" |
| **Steps** | How to reproduce? | "1. Create organism 2. Call evolve(-5)" |
| **Expected** | What should happen? | "Should raise ValueError" |
| **Actual** | What does happen? | "Crashes with TypeError" |
| **Environment** | Your setup | "Ubuntu 22.04, Python 3.11" |
| **Code** | Minimal example | 5-10 lines reproducing bug |
| **Error** | Full traceback | Complete error message |
| **Solution** | Ideas (optional) | "Add validation check" |

## 🔍 Common Mistakes to Avoid

### 1. Empty Templates
❌ Don't submit the template without filling it in
✅ Fill all required fields with specific information

### 2. Too Vague
❌ "Add better features"
✅ "Add real-time monitoring dashboard with WebSocket support"

### 3. No Context
❌ "It crashes"
✅ "Crashes when calling evolve() with negative generations (see code)"

### 4. Missing Code
❌ "The evolution function has a bug"
✅ Include 5-10 lines of code that reproduce the bug

### 5. Wrong Template
❌ Using Bug Report for feature requests
✅ Choose the template that matches your issue type

## 🚀 After Submitting

### Response Times
- **Critical bugs**: 24-48 hours
- **Feature requests**: 1-2 weeks
- **Questions**: 2-3 days
- **Documentation**: 1 week

### Auto-Labeling
Issues are automatically labeled based on:
- Template type (bug, enhancement, question, documentation)
- Keywords in title and description
- IP classification relevance

### Community Discussion
- Other users may comment with similar experiences
- Maintainers may ask for clarification
- You may be asked to test fixes

## 📚 Resources

- [Contributing Guide](../CONTRIBUTING.md) - How to contribute to DAIOF
- [IP Classification](../INTELLECTUAL_PROPERTY_CLASSIFICATION.md) - Understanding intellectual property
- [Documentation](https://nguyencuong1989.github.io/DAIOF-Framework/) - Full framework docs
- [Examples](../examples/) - Code examples
- [Discussions](https://github.com/NguyenCuong1989/DAIOF-Framework/discussions) - Community forum

## ❓ Still Unsure?

If you're unsure which template to use or how to describe your issue:

1. **Start with Discussions**: Post in [GitHub Discussions](https://github.com/NguyenCuong1989/DAIOF-Framework/discussions)
2. **Ask the Community**: Other users can help clarify
3. **Draft First**: Write your issue in a text editor first
4. **Review Examples**: Look at well-written issues for inspiration

---

**Attribution:** Powered by HYPERAI Framework  
**Creator:** Nguyễn Đức Cường (alpha_prime_omega)  
**Framework Created:** October 30, 2025
