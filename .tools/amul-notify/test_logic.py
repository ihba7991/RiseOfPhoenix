#!/usr/bin/env python3
"""
Offline tests for the parts of check_stock.py that don't need the network:
availability parsing, restock-transition detection, and message building.

The live API can't be exercised from CI without hitting Amul, so these lock
down the logic that decides *whether* to message — the part that would
otherwise spam a phone every 10 minutes if it regressed.

Run: python3 .tools/amul-notify/test_logic.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from check_stock import (  # noqa: E402
    FLAVOUR_RE,
    PACK_RE,
    build_message,
    is_available,
    load_state,
    save_state,
)

failures: list[str] = []


def check(name: str, got: object, want: object) -> None:
    if got != want:
        failures.append(f"{name}: got {got!r}, want {want!r}")
        print(f"  FAIL {name}: got {got!r}, want {want!r}")
    else:
        print(f"  ok   {name}")


print("is_available")
check("available=1, qty=5", is_available({"available": 1, "inventory_quantity": 5}), True)
check("available=1, qty=0", is_available({"available": 1, "inventory_quantity": 0}), False)
check("available=0, qty=9", is_available({"available": 0, "inventory_quantity": 9}), False)
check("available=1, no qty", is_available({"available": 1}), True)
check("empty product", is_available({}), False)
check("qty as string", is_available({"available": 1, "inventory_quantity": "3"}), True)
check("qty junk falls back", is_available({"available": 1, "inventory_quantity": "n/a"}), True)

print("\nname matching (alias-rename recovery)")
choc30 = "Amul Chocolate Whey Protein, 34 g | Pack of 30 sachets"
choc60 = "Amul Chocolate Whey Protein, 34 g | Pack of 60 sachets"
plain30 = "Amul Whey Protein, 32 g | Pack of 30 Sachets"
choc10 = "Amul Chocolate Whey Protein Gift Pack, 34 g | Pack of 10 sachets"


def matches(name: str) -> bool:
    return bool(FLAVOUR_RE.search(name) and PACK_RE.search(name))


check("chocolate 30 matches", matches(choc30), True)
check("chocolate 60 matches", matches(choc60), True)
check("plain 30 rejected (not chocolate)", matches(plain30), False)
check("chocolate 10 rejected (wrong pack)", matches(choc10), False)

print("\nrestock transition")


def transitions(previous: dict[str, bool], current: dict[str, bool]) -> list[str]:
    """Mirror of the main loop's notify rule."""
    return [a for a, avail in sorted(current.items()) if avail and not previous.get(a, False)]


check("oos -> in stock notifies", transitions({"a": False}, {"a": True}), ["a"])
check("in stock -> in stock silent", transitions({"a": True}, {"a": True}), [])
check("in stock -> oos silent", transitions({"a": True}, {"a": False}), [])
check("unseen + in stock notifies", transitions({}, {"a": True}), ["a"])
check("sell-out then restock re-notifies", transitions({"a": False}, {"a": True}), ["a"])
check("only the restocked one", transitions({"a": True, "b": False}, {"a": True, "b": True}), ["b"])

print("\nstate round-trip")
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "nested" / "state.json"
    check("missing file -> empty dict", load_state(path), {})
    save_state(path, {"in_stock": {"a": True}, "store": "karnataka"})
    check("round-trips", load_state(path)["in_stock"], {"a": True})
    path.write_text("{ not json")
    check("corrupt file -> empty dict", load_state(path), {})

print("\nmessage building")
msg = build_message(
    [
        {
            "alias": "amul-chocolate-whey-protein-34-g-or-pack-of-30-sachets",
            "name": choc30,
            "inventory_quantity": 12,
            "price": 1050,
        }
    ],
    "karnataka",
)
check("includes product name", choc30 in msg, True)
check("includes buy link", "shop.amul.com/en/product/" in msg, True)
check("includes qty", "12 left" in msg, True)
check("includes price", "₹1050" in msg, True)
check("includes store", "karnataka" in msg, True)

msg_no_qty = build_message([{"alias": "x", "name": "Choc 60"}], "karnataka")
check("survives missing qty/price", "Choc 60" in msg_no_qty and "left" not in msg_no_qty, True)

print()
if failures:
    print(f"{len(failures)} failure(s)")
    sys.exit(1)
print("all tests passed")
