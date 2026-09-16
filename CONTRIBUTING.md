# Contributing to PQC Crypto Inventory Lab

Thank you for your interest in contributing to PQC Crypto Inventory Lab! This project is designed as an educational tool for cryptographic inventory, PQC migration triage, and crypto agility assessment.

## How to Contribute

### Reporting Bugs or Feature Requests
- Check the [Issues](https://github.com/moruku36/pqc-crypto-inventory-lab/issues) tab to see if your topic is already being discussed.
- If not, open a new Issue using the appropriate issue template.
- For security vulnerabilities, please refer to [SECURITY.md](SECURITY.md) instead of creating a public issue.

### Development Setup
1. Fork and clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or .venv\Scripts\activate on Windows
   ```
3. Install dependencies in editable mode with development tools:
   ```bash
   python -m pip install -e ".[dev]"
   ```

### Code Quality and Verification
Before submitting a pull request, ensure all tests and quality checks pass:
```bash
python -m pytest -q
python -m ruff check .
python -m mypy
```

### Pull Request Guidelines
- Branch from `main` and use descriptive branch names.
- Keep commits focused and provide clear commit messages.
- Ensure no private keys, credentials, or sensitive customer filenames are included in sample files or tests.
- Update documentation in `docs/` and `README.md` if your change modifies CLI options, schemas, or assessment criteria.
