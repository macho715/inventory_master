# /automate pre-commit+ci

## What it does
- Installs pre-commit hooks
- Runs local lint/test sanity checks
- Prints next steps for enabling branch protection

## Commands (Windows PowerShell)
```powershell
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit run --all-files
pytest -q
```
