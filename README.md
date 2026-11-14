# Task Manager (code review demo)

A small, working to-do app: Flask + SQLite backend, vanilla JS frontend.
It contains **6 intentional issues** (see `EXPECTED_FINDINGS.md`) for evaluating a code review platform.

> ⚠️ Intentionally flawed. Run locally only, never deploy.

## Run
```bash
cd backend
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```
Admin token for "Clear all": `admin123`

## Features
- Add / toggle / delete tasks, search, live stats
- "Clear all" protected by an admin token

## Evaluate your review tool
Export your platform's findings as JSON (`file`, `line`, ...) then:
```bash
python tools/compare.py platform_output.json
```
Line numbers in `expected_findings.json` go stale if you edit the source.
