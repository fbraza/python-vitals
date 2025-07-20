# CLAUDE.md - Project Guidelines for Claude Code

## Project Overview
This repository contains biomarker algorithms for health assessment, including PhenoAge, SCORE2, and SCORE2-Diabetes cardiovascular risk calculations.

## Environment Setup
**IMPORTANT**: This project uses UV for dependency management. Before starting work:
```bash
# Sync dependencies and activate virtual environment
uv sync

# Activate the virtual environment (if not automatically activated)
source .venv/bin/activate
```

## Python Style Guidelines
**CRITICAL**: Follow the principles from `/vitals/specs/coding_style.md`. DO NOT OVERENGINEER. Always find the right balance between clarity and complexity.

### Core Principles (from specs/coding_style.md)
1. **Favor Simplicity Over Complexity**
   - Always choose simple, straightforward solutions
   - Avoid over-engineering and elaborate abstractions
   - No premature optimization
   - If there are two ways to solve a problem, choose the easier to understand

2. **Clarity is Key**
   - Readable code beats clever code
   - Use clear, descriptive names
   - Reduce cognitive load
   - Code should express intent clearly at a glance

3. **Write Pythonic Code**
   - Follow Python community standards and idioms
   - Use list comprehensions, generators, context managers appropriately
   - Write code that looks like Python wrote it

4. **Don't Repeat Yourself (DRY)**
   - Avoid code duplication
   - Use functions and modules for common logic
   - But don't abstract too early

5. **Focus on Readability First**
   - PEP8 is a guide, not a law
   - Readability trumps mechanical adherence to style rules
   - Consider the human reader first

6. **Embrace Conventions**
   - Follow established patterns consistently
   - Use PEP8 as baseline but prioritize readability

### Type Hints Guidelines
**IMPORTANT**: Do not overengineer type hints. Find the right balance:
- Use type hints for function signatures and class attributes
- Keep type hints simple and readable
- Don't create complex type aliases unless they add clarity
- Avoid overly generic or abstract type definitions
- If a type hint makes code harder to read, reconsider it

## Project Structure
```
vitals/
├── biomarkers/          # Common biomarker utilities
│   ├── helpers.py       # Helper functions for biomarker extraction
│   └── io.py           # Input/output utilities
├── models/             # Algorithm implementations
│   ├── phenoage.py     # PhenoAge calculation logic
│   ├── score2.py       # SCORE2 calculation logic
│   └── score2_diabetes.py  # SCORE2-Diabetes calculation logic
├── schemas/            # Pydantic models organized by algorithm
│   ├── phenoage.py     # PhenoAge-specific schemas
│   └── score2.py       # SCORE2 and SCORE2-Diabetes schemas
└── specs/              # Project specifications
    ├── coding_style.md # Python coding style guide
    ├── score2.md       # SCORE2 algorithm specification
    └── score2_diabetes.md  # SCORE2-Diabetes algorithm specification
```

## Development Workflow

### Before Starting Work
1. Sync dependencies: `uv sync`
2. Activate virtual environment: `source .venv/bin/activate` (if not auto-activated)
3. Ensure git hooks are installed: `make install` (this also installs pre-commit hooks)

### Running Tests
```bash
# Run tests with coverage report
make test

# Run linting
make lint
```

### Git Commit Process
**CRITICAL**: Before ANY commit:
1. Ensure pre-commit hooks are active (installed via `make install`)
2. If pre-commit hooks are not running automatically:
   - STOP and inform that git hooks need to be activated
   - Uncommit any changes
   - Run: `make install` to install pre-commit hooks
3. Pre-commit will run:
   - Code formatting (black, isort)
   - Linting (flake8, mypy)
   - Other configured checks

### Code Quality Checks
Before committing changes, ensure:
- [ ] Virtual environment is activated
- [ ] Code follows the style guidelines in `/vitals/specs/coding_style.md`
- [ ] Type hints are balanced (not overengineered)
- [ ] All functions have clear docstrings
- [ ] No unnecessary code duplication
- [ ] Variable and function names are descriptive
- [ ] Tests pass: `make test`
- [ ] Linting passes: `make lint`
- [ ] Pre-commit hooks pass

## Common Patterns
- Use Pydantic BaseModel for data validation
- Extract biomarkers using `biomarkers.helpers.extract_biomarkers_from_json()`
- Algorithm implementations go in `models/` directory
- Algorithm-specific schemas go in `schemas/` directory
- Use boolean types for binary values, not integers
- Keep type hints simple and practical

## Testing Approach
When implementing new features:
1. Check for existing test patterns in the codebase
2. Write tests that are simple and clear
3. Ensure edge cases are handled properly
4. Validate calculations against known results when possible
5. Run tests before committing: `make test`

## Important Notes
- The SCORE2 implementation uses Belgium (Low Risk region) calibration by default
- The SCORE2-Diabetes implementation includes diabetes-specific risk adjustments
- Binary values (sex, smoking, diabetes) should use boolean types in schemas
- Always handle potential ValueError exceptions when extracting biomarkers
- Balance code quality with pragmatism - don't overengineer solutions
