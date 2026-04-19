# ─── Sandbox: Workshop Objects (OOP) ────────────────────────────────────────
# Analogy: A blueprint (class) describes a tool type.
# Each manufactured copy (instance) has its own state.

class Tool:
    def __init__(self, name: str, available: bool = True) -> None:
        self.name      = name
        self.available = available

    def checkout(self) -> None:        # <── EXPLORE: raise error if not available
        self.available = False

    def return_tool(self) -> None:     # <── EXPLORE: add returned_by: str parameter
        self.available = True

    def __repr__(self) -> str:
        status = "free" if self.available else "in use"
        return f"Tool({self.name!r}, {status})"


# ─── CREATE ──────────────────────────────────────────────────────────────────
# Add a User class with name and borrowed_tools list.
# User.borrow(tool) should call tool.checkout() and add to borrowed_tools.
# User.return_all() should return every borrowed tool.

class User:
    def __init__(self, name: str) -> None:
        self.name           = name
        self.borrowed_tools: list[Tool] = []

    def borrow(self, tool: Tool) -> None:
        tool.checkout()
        self.borrowed_tools.append(tool)

    def return_all(self) -> None:
        for t in self.borrowed_tools:
            t.return_tool()
        self.borrowed_tools.clear()


if __name__ == "__main__":
    hammer = Tool("hammer")
    ravi   = User("Ravi")
    ravi.borrow(hammer)
    print(hammer)        # Tool('hammer', in use)
    ravi.return_all()
    print(hammer)        # Tool('hammer', free)
