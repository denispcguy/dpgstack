# UV
Package manager
## Workflow: Exporting into `requirements.txt`
1. Make sure `pyproject.toml` has the requirements.
2. Run `uv export --no-dev -o requirements.txt`. Dev ones will be ignored.
3. `requirements.txt` appears in project root.