# ─── Silent Teacher ──────────────────────────────────────────────────────────
import importlib, sys, types

# Reload cleanly so edits in main.py are picked up each run
if 'main' in sys.modules:
    del sys.modules['main']
import main

assert hasattr(main, 'owner_full'), "Missing owner_full – did you create the bin?"
assert isinstance(main.owner_full, str), "owner_full must be text (str)"
assert len(main.owner_full.split()) >= 2, "owner_full should combine first AND last name"
print("\u2705 Lesson 1 complete: The Storage Box mastered!")
