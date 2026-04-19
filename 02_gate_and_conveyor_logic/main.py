# ─── Sandbox: The Gate and Conveyor ─────────────────────────────────────────
# Analogy: A security gate decides who passes (if/elif/else).
# A conveyor belt moves every item in a list (for loop).

codes = ["ok", "warn", "ok", "fail", "ok"]  # <── EXPLORE: add more codes

fail_count = 0
for code in codes:
    if code == "fail":
        print("\u26a0 Stop line")
        fail_count += 1
    elif code == "warn":              # <── EXPLORE: add this branch
        print("\U0001f7e1 Warning – slow down")
    else:
        print("\u2705 Continue")

print(f"Total failures: {fail_count}")

# ─── CREATE ──────────────────────────────────────────────────────────────────
# Write a function validate_password(pw: str) -> bool
# Rules: length >= 8, contains at least one digit, contains at least one uppercase.

def validate_password(pw: str) -> bool:
    if len(pw) < 8:
        return False
    if not any(c.isdigit() for c in pw):
        return False
    if not any(c.isupper() for c in pw):
        return False
    return True

print(validate_password("Abcdef12"))   # expected True
print(validate_password("short"))      # expected False
