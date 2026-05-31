#!/usr/bin/env python3
"""
Scaffold per-item folders under each LLD tracker.

For each entry in the design-patterns / machine-coding / concurrency
trackers, create a folder containing a README.md with the problem
statement and a note on how to bootstrap a Java workspace using
.tools/init-java.sh.

Folder layout per person:

    <person>/lld/design-patterns/<kind>/<slug>/README.md
    <person>/lld/machine-coding/<NN-slug>/README.md
    <person>/lld/concurrency/<category>/<slug>/README.md

The data here mirrors what's hardcoded in the corresponding tracker
HTML files — keep them in sync.

Run from the repo root:

    python3 .tools/scaffold-lld.py
"""

from __future__ import annotations

import re
from pathlib import Path

PEOPLE = ["ihba7991", "vikku"]

# ---------------------------------------------------------------------------
# Data (mirrors the JS literals in lld/*.html)
# ---------------------------------------------------------------------------

DESIGN_PATTERNS: dict[str, list[tuple[str, str]]] = {
    "creational": [
        ("Abstract Factory",
         "Provide an interface for creating families of related objects without specifying their concrete classes."),
        ("Builder",
         "Separate the construction of a complex object from its representation so the same process can create different representations."),
        ("Factory Method",
         "Define an interface for creating an object, but let subclasses decide which class to instantiate."),
        ("Prototype",
         "Specify the kinds of objects to create using a prototypical instance, then create new objects by copying it."),
        ("Singleton",
         "Ensure a class has only one instance, and provide a global point of access to it."),
    ],
    "structural": [
        ("Adapter",   "Convert the interface of a class into another interface clients expect."),
        ("Bridge",    "Decouple an abstraction from its implementation so the two can vary independently."),
        ("Composite", "Compose objects into tree structures to represent part-whole hierarchies; clients treat individual objects and compositions uniformly."),
        ("Decorator", "Attach additional responsibilities to an object dynamically; a flexible alternative to subclassing."),
        ("Facade",    "Provide a unified interface to a set of interfaces in a subsystem."),
        ("Flyweight", "Use sharing to support large numbers of fine-grained objects efficiently."),
        ("Proxy",     "Provide a surrogate or placeholder for another object to control access to it."),
    ],
    "behavioral": [
        ("Chain of Responsibility", "Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle it."),
        ("Command",                 "Encapsulate a request as an object, letting you parameterize clients with different requests and support undo."),
        ("Interpreter",             "Given a language, define a representation for its grammar along with an interpreter that uses the representation."),
        ("Iterator",                "Provide a way to access elements of an aggregate object sequentially without exposing its underlying representation."),
        ("Mediator",                "Define an object that encapsulates how a set of objects interact, promoting loose coupling."),
        ("Memento",                 "Without violating encapsulation, capture and externalize an object's internal state so it can be restored later."),
        ("Observer",                "Define a one-to-many dependency so that when one object changes state, all dependents are notified and updated."),
        ("State",                   "Allow an object to alter its behavior when its internal state changes; it appears to change its class."),
        ("Strategy",                "Define a family of algorithms, encapsulate each one, and make them interchangeable."),
        ("Template Method",         "Define the skeleton of an algorithm in an operation, deferring some steps to subclasses."),
        ("Visitor",                 "Represent an operation to be performed on the elements of an object structure without changing the classes of the elements."),
    ],
}

MACHINE_CODING: list[tuple[str, int, str, str, str]] = [
    # (n, tier, name, tag, time)
    ("01", 1, "Tic-Tac-Toe",             "Classic 2-player board. Win/draw detection.",                    "45 min"),
    ("02", 1, "Snake & Ladder",          "Dice + board + multiple players. Pure state machine.",           "60 min"),
    ("03", 1, "Vending Machine",         "State pattern (Idle → HasCoin → Dispensing).",                   "60 min"),
    ("04", 1, "Logger",                  "Async logger, log levels, appenders (file, console).",           "45 min"),
    ("05", 1, "Stack Overflow Lite",     "Questions, answers, votes, tags. In-memory.",                    "75 min"),
    ("06", 2, "Parking Lot",             "Multi-level, slot types, ticketing. Bedrock LLD problem.",       "90 min"),
    ("07", 2, "Splitwise",               "Expense splitting, simplify debts (graph reduction).",           "90 min"),
    ("08", 2, "LRU Cache",               "Map + doubly-linked list. O(1) get/put.",                        "45 min"),
    ("09", 2, "LFU Cache",               "Frequency buckets + DLL per bucket.",                            "75 min"),
    ("10", 2, "Rate Limiter",            "Token bucket, leaky bucket, sliding window — pick one each.",    "75 min"),
    ("11", 2, "ATM",                     "Card → PIN → transaction. State machine + cash inventory.",      "75 min"),
    ("12", 2, "Chess",                   "Piece hierarchy, move validation, check/checkmate.",             "120 min"),
    ("13", 2, "Library Mgmt",            "Books, members, reservations, fines. Pure CRUD + state.",        "75 min"),
    ("14", 2, "Elevator System",         "SCAN algorithm, multi-car coordination, request queue.",         "90 min"),
    ("15", 2, "Notification System",     "Strategy pattern across SMS/Email/Push. Retry + dedupe.",        "75 min"),
    ("16", 2, "In-memory DB",            "Transactions: begin/commit/rollback, nested savepoints.",        "90 min"),
    ("17", 2, "Inventory System",        "Stock, reservations, multiple warehouses, low-stock alerts.",    "90 min"),
    ("18", 3, "BookMyShow",              "Cinemas, shows, seat locking with TTL. Concurrency-heavy.",      "2 hrs"),
    ("19", 3, "Food Ordering",           "Zomato/Swiggy clone. Restaurant catalog → cart → order lifecycle.","2 hrs"),
    ("20", 3, "Ride Sharing",            "Uber clone. Matching, surge pricing, trip lifecycle, payments.", "2 hrs"),
    ("21", 3, "Hotel Booking",           "Rooms, rate plans, availability calendar, overbooking guard.",   "2 hrs"),
    ("22", 3, "File System",             "Path resolution, inodes, hard/symbolic links, mkdir/ls/touch.",  "90 min"),
    ("23", 3, "Stock Exchange",          "Order book, matching engine, price-time priority.",              "2 hrs"),
    ("24", 3, "Cab Aggregator Pricing",  "Surge model, demand zones, cohort discounting.",                 "90 min"),
    ("25", 3, "Distributed Task Queue",  "Producer/worker/queue, retries, DLQ, scheduling.",               "2 hrs"),
]

CONCURRENCY: dict[str, list[tuple[str, str]]] = {
    "primitives": [
        ("Threads & Runnable",            "Spin up a thread, join it, understand daemon vs user threads."),
        ("synchronized + monitors",       "Intrinsic locks, reentrancy, monitor enter/exit semantics."),
        ("volatile",                      "Visibility guarantees and the difference vs atomicity."),
        ("ReentrantLock",                 "Explicit lock with tryLock, lockInterruptibly, fair locks."),
        ("Semaphore",                     "Permits, fair semantics, used for throttling."),
        ("CountDownLatch / CyclicBarrier","One-shot vs reusable rendezvous points."),
        ("Atomic classes",                "AtomicInteger, compareAndSet, ABA problem."),
        ("ThreadLocal",                   "Per-thread storage, leaks via thread pools, InheritableThreadLocal."),
    ],
    "patterns": [
        ("Producer–Consumer",          "BlockingQueue based; bounded buffer with wait/notify variant."),
        ("Thread Pool",                "Implement a fixed pool with a BlockingQueue + worker threads."),
        ("Reader–Writer Lock",         "Many readers OR one writer. Fairness and starvation."),
        ("Future / Promise",           "Submit work, get a handle; chain with thenApply."),
        ("CompletableFuture pipeline", "Compose async stages with thenCompose, allOf, exceptionally."),
        ("Fork–Join",                  "Recursive work-stealing pool, RecursiveTask example."),
        ("Async pipeline / Pub-Sub",   "Decouple producers and consumers across stages."),
        ("Double-checked Singleton",   "Why volatile is required; lazy holder idiom alternative."),
    ],
    "classics": [
        ("Dining Philosophers",      "Avoid deadlock via ordering / waiter / asymmetric pickup."),
        ("Sleeping Barber",          "Coordinate barber, customers, and waiting room."),
        ("Cigarette Smokers",        "Three smokers, an agent, mutexes per ingredient."),
        ("H2O Synchronization",      "Build water molecules from H and O threads."),
        ("Print FooBar alternately", "Strict ordering between two threads using locks/semaphores."),
        ("ZeroEvenOdd",              "Three threads cooperate to print 0,1,0,2,0,3…"),
        ("Building H2O / molecules", "Generalize H2O to arbitrary molecule formulas."),
    ],
    "memory": [
        ("Java Memory Model basics", "happens-before, partial order, reordering."),
        ("Visibility vs atomicity",  "Two distinct guarantees often conflated."),
        ("Synchronization actions",  "Locks, volatile writes, final field publication."),
        ("Safe publication",         "Final fields, volatile, immutable objects."),
        ("Cache coherence basics",   "MESI, false sharing, padding strategies."),
        ("CAS & lock-free queues",   "Treiber stack, Michael-Scott queue."),
        ("Memory leaks via locks",   "Forgotten ThreadLocals, unbounded queues, deadlocks."),
    ],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slug(text: str) -> str:
    """Lowercase, replace non-alnum runs with single hyphen, strip ends."""
    return _SLUG_RE.sub("-", text.lower()).strip("-")


README_TEMPLATE = """\
# {title}

{statement}

## Bootstrap a Java workspace

From inside this folder:

```bash
bash "$(git rev-parse --show-toplevel)/.tools/init-java.sh"
```

That creates `src/Main.java`, a `run.sh` compile-and-run wrapper, and a
`.gitignore`. Edit `src/Main.java`, add more classes under `src/` as you
need, then run `./run.sh`.

When you're done, tick the box in [`{tracker_relpath}`]({tracker_relpath}).
"""


def write_readme(folder: Path, title: str, statement: str, tracker_relpath: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    body = README_TEMPLATE.format(
        title=title,
        statement=statement,
        tracker_relpath=tracker_relpath,
    )
    (folder / "README.md").write_text(body, encoding="utf-8")


# ---------------------------------------------------------------------------
# Per-tracker scaffolding
# ---------------------------------------------------------------------------

def scaffold_design_patterns(lld_root: Path) -> int:
    n = 0
    base = lld_root / "design-patterns"
    for kind, items in DESIGN_PATTERNS.items():
        for name, intent in items:
            folder = base / kind / slug(name)
            # tracker is at <person>/lld/design-patterns.html; we are 3 levels down
            write_readme(folder, name, intent, "../../../design-patterns.html")
            n += 1
    return n


def scaffold_machine_coding(lld_root: Path) -> int:
    n = 0
    base = lld_root / "machine-coding"
    for num, tier, name, tag, time in MACHINE_CODING:
        folder = base / f"{num}-{slug(name)}"
        statement = f"**Tier {tier} · ~{time}**\n\n{tag}"
        # tracker is at <person>/lld/machine-coding.html; we are 2 levels down
        write_readme(folder, name, statement, "../../machine-coding.html")
        n += 1
    return n


def scaffold_concurrency(lld_root: Path) -> int:
    n = 0
    base = lld_root / "concurrency"
    for category, items in CONCURRENCY.items():
        for name, intent in items:
            folder = base / category / slug(name)
            # tracker is at <person>/lld/concurrency.html; we are 3 levels down
            write_readme(folder, name, intent, "../../../concurrency.html")
            n += 1
    return n


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    for who in PEOPLE:
        lld = repo_root / who / "lld"
        dp = scaffold_design_patterns(lld)
        mc = scaffold_machine_coding(lld)
        cc = scaffold_concurrency(lld)
        print(f"{who}: {dp} design-patterns · {mc} machine-coding · {cc} concurrency")
    print("✓ done — run `bash $(git rev-parse --show-toplevel)/.tools/init-java.sh`"
          " inside any item folder to bootstrap a Java workspace.")


if __name__ == "__main__":
    main()
