# ─── Silent Teacher ──────────────────────────────────────────────────────────
import sys
if 'main' in sys.modules:
    del sys.modules['main']
import main

assert callable(main.validate_password), "validate_password must be a function"
assert main.validate_password("Abcdef12") is True,  "'Abcdef12' meets all rules"
assert main.validate_password("short")    is False, "'short' is too short"
assert main.validate_password("alllower1") is False, "no uppercase fails"
assert main.validate_password("NoDigitHere") is False, "no digit fails"
print("\u2705 Lesson 2 complete: Gate and Conveyor mastered!")
