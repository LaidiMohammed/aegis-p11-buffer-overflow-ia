import sys
sys.path.insert(0, r'C:\Users\pc\Documents\M1\IACS\Project_EthicalHacking\aegis-p11-buffer-overflow-ia')
from pathlib import Path
from unittest.mock import patch
import contextlib, io, json

import buffer_overflow_ia_main as m

# Test 1: smoke
out = m.smoke("x", "y")
assert out["ok"] is True
print("PASS: test_smoke_structure")

# Test 2: main returns 0
ret = m.main([])
assert ret == 0
print("PASS: test_main_returns_0")

# Test 3: main --json with --file
with contextlib.redirect_stdout(io.StringIO()) as buf:
    ret = m.main(["--json", "--file", "test_sample.c"])
data = json.loads(buf.getvalue())
assert data["project"] == "P11"
print("PASS: test_main_json_output with --file")

# Test 4: main --json without --file (should use default)
with contextlib.redirect_stdout(io.StringIO()) as buf:
    ret = m.main(["--json"])
data = json.loads(buf.getvalue())
assert data["project"] == "P11"
print("PASS: test_main_json_output without --file (default)")

print("\nAll P11 tests passed!")