# ─── Sandbox: The Notebook Ledger ────────────────────────────────────────────
# Analogy: A paper ledger is written in order. Mistakes don't crash the ledger;
# they are crossed out and corrected on the next line.

from pathlib import Path

LEDGER = Path("notes.txt")


def save_note(line: str) -> None:        # <── EXPLORE: accept path as parameter
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def read_notes() -> list:
    try:
        return LEDGER.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []                        # <── EXPLORE: log a warning here


# ─── CREATE ──────────────────────────────────────────────────────────────────
# Add delete_last_note() that removes the final line from the ledger file.

def delete_last_note() -> None:
    lines = read_notes()
    if lines:
        LEDGER.write_text("\n".join(lines[:-1]) + ("\n" if len(lines) > 1 else ""), encoding="utf-8")


if __name__ == "__main__":
    save_note("Python is a tool, not a goal.")
    save_note("Write readable code for the next reader.")
    print(read_notes())
