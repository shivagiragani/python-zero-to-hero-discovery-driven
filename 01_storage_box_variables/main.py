# ─── Sandbox: The Storage Box ───────────────────────────────────────────────
# Analogy: Labeled bins in a workshop workshop. Each bin can hold exactly one
# thing and you find it by its label – never by poking around.

item_label = "Hammer"      # <── EXPLORE: rename this variable everywhere
item_count = 3             # <── EXPLORE: change to int(input(...))

print(f"{item_label}: {item_count}")

# ─── CREATE ──────────────────────────────────────────────────────────────────
# Add three bins: owner_first, owner_last, owner_full
# owner_full should join first and last with a space.
# Example: owner_full = owner_first + " " + owner_last

owner_first = "Ada"
owner_last  = "Lovelace"
owner_full  = owner_first + " " + owner_last

print(f"Owner: {owner_full}")
