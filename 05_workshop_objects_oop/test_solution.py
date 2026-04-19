# ─── Silent Teacher ──────────────────────────────────────────────────────────
import sys
if 'main' in sys.modules:
    del sys.modules['main']
import main

t = main.Tool("saw")
assert t.available is True
t.checkout()
assert t.available is False
t.return_tool()
assert t.available is True

u = main.User("Asha")
u.borrow(t)
assert t.available is False
assert t in u.borrowed_tools
u.return_all()
assert t.available is True
assert u.borrowed_tools == []
print("\u2705 Lesson 5 complete: Workshop Objects mastered!")
