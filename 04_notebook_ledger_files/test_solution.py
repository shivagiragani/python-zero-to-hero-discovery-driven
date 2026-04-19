# ─── Silent Teacher ──────────────────────────────────────────────────────────
import sys
from pathlib import Path
if 'main' in sys.modules:
    del sys.modules['main']
import main

test_file = Path("test_notes_tmp.txt")
main.LEDGER = test_file               # point at temp file

main.save_note("hello")
main.save_note("world")
data = main.read_notes()
assert "hello" in data, "save_note or read_notes broken"
assert len(data) == 2, "expected 2 lines"

main.delete_last_note()
assert main.read_notes() == ["hello"], "delete_last_note should remove last line"

test_file.unlink(missing_ok=True)
print("\u2705 Lesson 4 complete: Notebook Ledger mastered!")
