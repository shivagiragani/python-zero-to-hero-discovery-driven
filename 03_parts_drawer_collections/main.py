# ─── Sandbox: The Parts Drawer ───────────────────────────────────────────────
# Analogy: A drawer system. Each drawer (dict key) holds one type of part
# (value). You never empty the drawer yourself – a function does it.

def summarize_cart(cart: dict) -> int:
    """Return total item count."""
    return sum(cart.values())         # <── EXPLORE: also return total price

cart = {"pen": 2, "notebook": 3, "ruler": 1}  # <── EXPLORE: add more items
print(f"Total items: {summarize_cart(cart)}")

# ─── CREATE ──────────────────────────────────────────────────────────────────
# Build a function lookup_contact(contacts: dict, name: str) -> str | None
# Return phone number if found, or None if not.

contacts = {
    "Asha": "9876543210",
    "Ravi": "9123456789",
}

def lookup_contact(contacts: dict, name: str):
    return contacts.get(name)

print(lookup_contact(contacts, "Asha"))    # expected 9876543210
print(lookup_contact(contacts, "Meera"))   # expected None
