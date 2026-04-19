# ─── Sandbox: The Inventory Shelf (SQLAlchemy) ───────────────────────────────
# Analogy: Each row in a database table is a labeled shelf slot.
# SQLAlchemy is the automated clerk who reads and writes slots for you.
#
# DB URL is driven by env var DATABASE_URL (defaults to SQLite).

from __future__ import annotations
import os
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///items.db")

engine       = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base         = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id       = Column(Integer, primary_key=True)
    name     = Column(String(120), nullable=False)
    quantity = Column(Integer, default=0)   # <── EXPLORE: add category column


Base.metadata.create_all(engine)


def add_item(name: str, quantity: int = 1) -> Item:
    with SessionLocal() as session:
        item = Item(name=name, quantity=quantity)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def list_items() -> list[Item]:
    with SessionLocal() as session:
        return session.execute(select(Item)).scalars().all()


# ─── CREATE ──────────────────────────────────────────────────────────────────
# Add update_quantity(item_id, new_qty) and delete_item(item_id).

if __name__ == "__main__":
    add_item("notebook", 10)
    for it in list_items():
        print(it.id, it.name, it.quantity)
