# ─── Silent Teacher ──────────────────────────────────────────────────────────
import sys
if 'main' in sys.modules:
    del sys.modules['main']
import main

assert main.summarize_cart({"a": 1, "b": 2}) == 3, "sum should be 3"
assert main.lookup_contact({"X": "123"}, "X") == "123", "known contact not found"
assert main.lookup_contact({"X": "123"}, "Y") is None, "unknown contact should be None"
print("\u2705 Lesson 3 complete: Parts Drawer mastered!")
