#!/usr/bin/env python3
"""Compare your platform's output with expected_findings.json.

Usage: python tools/compare.py platform_output.json [--tolerance 3]

platform_output.json: a list of objects with at least `file` and `line`
(optionally `type`, `severity`). Also accepts {"findings": [...]}.
A finding matches if same file and |line - expected_line| <= tolerance.
"""
import json, sys, os

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
tol = int(args[args.index("--tolerance") + 1]) if "--tolerance" in args else 3
here = os.path.dirname(os.path.abspath(__file__))
expected = json.load(open(os.path.join(here, "..", "expected_findings.json")))
found = json.load(open(args[0]))
if isinstance(found, dict):
    found = found.get("findings", [])

norm = lambda p: str(p).replace("\\", "/").lstrip("./")
used, tp, missed = set(), [], []
for e in expected:
    m = next((i for i, f in enumerate(found) if i not in used
              and norm(f.get("file", "")).endswith(e["file"])
              and abs(int(f.get("line", -999)) - e["line"]) <= tol), None)
    if m is None:
        missed.append(e)
    else:
        used.add(m); tp.append(e)
extra = [f for i, f in enumerate(found) if i not in used]

print(f"Expected: {len(expected)} | Detected: {len(tp)} | Missed: {len(missed)} | Extra: {len(extra)}")
print(f"Recall: {len(tp)/len(expected):.0%}  Precision(vs ground truth): {len(tp)/max(len(found),1):.0%}")
if missed:
    print("\nMISSED:")
    for e in missed:
        print(f"  {e['id']} {e['file']}:{e['line']} [{e['severity']}] {e['type']}")
if extra:
    print("\nEXTRA (review manually - could be false positives or valid extra issues):")
    for f in extra:
        print(f"  {f.get('file')}:{f.get('line')} {f.get('type', '')}")
