# Expected Findings (ground truth)

| ID | File | Line | Type | Severity | CWE |
|---|---|---|---|---|---|
| F01 | `backend/app.py` | 46 | SQL Injection | Critical | CWE-89 |
| F02 | `backend/app.py` | 9 | Hardcoded Secret | High | CWE-798 |
| F03 | `backend/app.py` | 97 | Division By Zero (Bug) | Medium | CWE-369 |
| F04 | `backend/app.py` | 103 | Security Misconfiguration | High | CWE-489 |
| F05 | `frontend/app.js` | 23 | Stored XSS | High | CWE-79 |
| F06 | `frontend/app.js` | 72 | Sensitive Data In localStorage | Medium | CWE-922 |

## Details

- **F01** `backend/app.py:46` - Search term concatenated into the SQL string; exploitable via /api/tasks?search=.
- **F02** `backend/app.py:9` - Admin token hardcoded in source and guards the destructive 'clear all' endpoint.
- **F03** `backend/app.py:97` - With no tasks, /api/stats raises ZeroDivisionError and returns HTTP 500.
- **F04** `backend/app.py:103` - Werkzeug debugger enabled while listening on 0.0.0.0 (remote code execution risk).
- **F05** `frontend/app.js:23` - Task title inserted via innerHTML without escaping; persists in the DB and runs for every visitor.
- **F06** `frontend/app.js:72` - Admin token persisted in localStorage, readable by any script (e.g. via the XSS above).
