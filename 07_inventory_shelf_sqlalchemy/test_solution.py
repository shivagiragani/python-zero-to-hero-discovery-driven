# ─── Silent Teacher ──────────────────────────────────────────────────────────
import os, sys
os.environ["DATABASE_URL"] = "sqlite:///test_items_tmp.db"
for mod in list(sys.modules.keys()):
    if 'main' in mod:
        del sys.modules[mod]

import main
main.Base.metadata.drop_all(main.engine)  # clean slate
main.Base.metadata.create_all(main.engine)

assert 'items' in main.Base.metadata.tables, "items table missing"
it = main.add_item("ruler", 5)
assert it.name == "ruler"
assert it.quantity == 5
assert len(main.list_items()) >= 1

import pathlib
pathlib.Path("test_items_tmp.db").unlink(missing_ok=True)
print("\u2705 Lesson 7 complete: Inventory Shelf mastered!")
