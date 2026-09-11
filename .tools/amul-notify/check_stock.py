#!/usr/bin/env python3
"""
Watch shop.amul.com for Amul chocolate whey protein and ping Telegram when
the 30- or 60-sachet packs come back in stock.

Amul stock is regional: the shop resolves your pincode to a "substore" and
every product's availability is reported for that substore only. So the run
order matters — bootstrap a session, set the store preference, and only then
ask about products. Asking first returns availability for the wrong region.

Only out-of-stock -> in-stock *transitions* are announced. The previous
result is kept in a small JSON state file so a 10-minute cron doesn't turn a
single restock into six identical messages an hour. A pack that is still in
stock on the next run is silently skipped; when it sells out the state resets
so the next restock alerts again.

Env:
  TELEGRAM_BOT_TOKEN   required unless --dry-run
  TELEGRAM_CHAT_ID     required unless --dry-run
  AMUL_PINCODE         default 560100
  AMUL_STORE           optional substore alias, skips pincode lookup
  AMUL_STATE_FILE      default .amul-state/state.json
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = "https://shop.amul.com"

# The two SKUs asked for. Aliases are the trailing path segment of the public
# product URL, e.g. shop.amul.com/en/product/<alias>.
TARGET_ALIASES = [
    "amul-chocolate-whey-protein-34-g-or-pack-of-30-sachets",
    "amul-chocolate-whey-protein-34-g-or-pack-of-60-sachets",
]

# Fallback used to spot chocolate 30/60 SKUs if Amul renames an alias. Applied
# to the protein category listing when a target alias stops resolving.
FLAVOUR_RE = re.compile(r"chocolate", re.I)
PACK_RE = re.compile(r"pack\s+of\s+(30|60)\s+sachets", re.I)

DEFAULT_PINCODE = "560100"
DEFAULT_STATE_FILE = ".amul-state/state.json"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

TIMEOUT = 30


def log(msg: str) -> None:
    print(msg, flush=True)


def make_tid() -> str:
    """Amul's frontend stamps a per-request trace id; the API rejects some
    calls without it. Shape is <base36 ms>:<counter>:<random hex>."""
    ms = int(time.time() * 1000)
    return f"{ms}:{random.randint(1, 1000)}:{os.urandom(16).hex()}"


def build_session() -> requests.Session:
    session = requests.Session()
    # A 10-minute cron will inevitably land on the odd 5xx or connection reset;
    # retry those rather than failing the whole run.
    retry = Retry(
        total=4,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "POST", "PUT"}),
        raise_on_status=False,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update(
        {
            "User-Agent": UA,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": BASE,
            "Referer": f"{BASE}/en/browse/protein",
        }
    )
    # Bootstrap cookies. The homepage call is what mints the session the
    # preference and product endpoints expect.
    session.get(f"{BASE}/", timeout=TIMEOUT)
    session.get(
        f"{BASE}/api/1/entity/ms.homepage",
        headers={"tid": make_tid()},
        timeout=TIMEOUT,
    )
    return session


def resolve_substore(session: requests.Session, pincode: str) -> str | None:
    """Map a pincode to its substore alias by scanning the substore list.

    Amul ships the pincode -> substore mapping to the browser, so this is a
    plain read. Returns None if the list can't be read or nothing matches,
    letting the caller fall back to AMUL_STORE.
    """
    try:
        resp = session.get(
            f"{BASE}/api/1/entity/ms.substore",
            params={"limit": 200, "fields[name]": 1, "fields[alias]": 1, "fields[pincodes]": 1},
            headers={"tid": make_tid()},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        rows = resp.json().get("data") or []
    except (requests.RequestException, ValueError) as exc:
        log(f"  substore lookup failed ({exc}); will fall back to AMUL_STORE")
        return None

    for row in rows:
        pincodes = row.get("pincodes") or []
        if isinstance(pincodes, str):
            pincodes = [p.strip() for p in pincodes.split(",")]
        if pincode in {str(p).strip() for p in pincodes}:
            alias = row.get("alias") or row.get("name")
            log(f"  pincode {pincode} -> substore '{alias}'")
            return alias

    log(f"  pincode {pincode} not found in {len(rows)} substores")
    return None


def set_store(session: requests.Session, store: str) -> None:
    """Pin the session to a substore so availability is reported for it."""
    resp = session.put(
        f"{BASE}/entity/ms.settings/_/setPreferences",
        json={"data": {"store": store}},
        headers={"tid": make_tid(), "Content-Type": "application/json"},
        timeout=TIMEOUT,
    )
    if resp.status_code >= 400:
        # Older builds of the shop accept POST here; try once before giving up.
        resp = session.post(
            f"{BASE}/entity/ms.settings/_/setPreferences",
            json={"data": {"store": store}},
            headers={"tid": make_tid(), "Content-Type": "application/json"},
            timeout=TIMEOUT,
        )
    resp.raise_for_status()
    log(f"  store preference set to '{store}'")


def fetch_product(session: requests.Session, alias: str) -> dict[str, Any] | None:
    resp = session.get(
        f"{BASE}/api/1/entity/ms.products",
        params={"q": json.dumps({"alias": alias}), "limit": 1},
        headers={"tid": make_tid()},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    rows = resp.json().get("data") or []
    return rows[0] if rows else None


def fetch_protein_category(session: requests.Session) -> list[dict[str, Any]]:
    """Whole protein category listing — used only to recover from a renamed
    alias, so failure here is non-fatal."""
    try:
        resp = session.get(
            f"{BASE}/api/1/entity/ms.products",
            params={
                "q": json.dumps({"categories": {"$in": ["protein"]}}),
                "limit": 100,
            },
            headers={"tid": make_tid()},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json().get("data") or []
    except (requests.RequestException, ValueError) as exc:
        log(f"  category listing failed ({exc})")
        return []


def is_available(product: dict[str, Any]) -> bool:
    """Amul reports `available` as 0/1; `inventory_quantity` is the count.

    Treat a product as buyable only when both agree, since `available` alone
    can lag behind a sell-out.
    """
    if not product.get("available"):
        return False
    qty = product.get("inventory_quantity")
    if qty is None:
        return True
    try:
        return int(qty) > 0
    except (TypeError, ValueError):
        return True


def product_url(alias: str) -> str:
    return f"{BASE}/en/product/{alias}"


def load_state(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def send_telegram(token: str, chat_id: str, text: str) -> None:
    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        },
        timeout=TIMEOUT,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Telegram {resp.status_code}: {resp.text[:300]}")


def build_message(restocked: list[dict[str, Any]], store: str) -> str:
    lines = ["🍫 <b>Amul chocolate whey protein is back in stock</b>", ""]
    for item in restocked:
        qty = item.get("inventory_quantity")
        qty_txt = f" — {qty} left" if qty not in (None, "") else ""
        price = item.get("price")
        price_txt = f" · ₹{price}" if price else ""
        lines.append(f'• <a href="{product_url(item["alias"])}">{item["name"]}</a>{price_txt}{qty_txt}')
    lines += ["", f"<i>Store: {store}</i>", "👉 Buy fast — these sell out in minutes."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="check stock and print, but never message Telegram or write state",
    )
    parser.add_argument(
        "--force-notify",
        action="store_true",
        help="message even if the pack was already in stock on the last run",
    )
    parser.add_argument(
        "--dump",
        action="store_true",
        help="print the raw product JSON (for fixing field names against the live API)",
    )
    args = parser.parse_args()

    pincode = os.environ.get("AMUL_PINCODE", DEFAULT_PINCODE).strip()
    state_file = Path(os.environ.get("AMUL_STATE_FILE", DEFAULT_STATE_FILE))

    log(f"Amul stock check · pincode {pincode}")
    session = build_session()

    store = os.environ.get("AMUL_STORE", "").strip() or resolve_substore(session, pincode)
    if not store:
        log(
            "ERROR: could not determine a substore. Set AMUL_STORE to the alias "
            "shown in the shop's store picker (e.g. 'karnataka')."
        )
        return 2
    set_store(session, store)

    # Resolve targets, recovering by name match if an alias has been renamed.
    found: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    for alias in TARGET_ALIASES:
        try:
            product = fetch_product(session, alias)
        except requests.RequestException as exc:
            log(f"ERROR: fetching {alias} failed: {exc}")
            return 2
        if product:
            found[alias] = product
        else:
            missing.append(alias)

    if missing:
        log(f"  {len(missing)} alias(es) did not resolve; scanning protein category")
        for product in fetch_protein_category(session):
            name = product.get("name") or ""
            alias = product.get("alias") or ""
            if FLAVOUR_RE.search(name) and PACK_RE.search(name) and alias not in found:
                log(f"  recovered by name match: {name} ({alias})")
                found[alias] = product

    if not found:
        log("ERROR: no matching products found — the API shape likely changed.")
        log("Re-run with --dump to inspect the raw response.")
        return 2

    if args.dump:
        log(json.dumps(list(found.values()), indent=2)[:8000])

    state = load_state(state_file)
    previous = state.get("in_stock", {})
    now_in_stock: dict[str, bool] = {}
    restocked: list[dict[str, Any]] = []

    for alias, product in sorted(found.items()):
        name = product.get("name") or alias
        available = is_available(product)
        now_in_stock[alias] = available
        was = bool(previous.get(alias, False))
        mark = "IN STOCK" if available else "out of stock"
        log(f"  [{mark:>12}] {name}")
        if available and (not was or args.force_notify):
            restocked.append({**product, "alias": alias, "name": name})

    if restocked:
        text = build_message(restocked, store)
        if args.dry_run:
            log("\n--- dry run, would send ---\n" + text)
        else:
            token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
            chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
            if not token or not chat_id:
                log("ERROR: TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID are not set.")
                return 2
            send_telegram(token, chat_id, text)
            log(f"\nNotified Telegram about {len(restocked)} pack(s).")
    else:
        log("\nNothing newly in stock; no message sent.")

    if not args.dry_run:
        state["in_stock"] = now_in_stock
        state["checked_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        state["store"] = store
        save_state(state_file, state)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except requests.RequestException as exc:
        # Network trouble is expected occasionally on a 10-minute cron; report
        # it in one line rather than a traceback so the job log stays readable.
        log(f"ERROR: could not reach {BASE}: {exc}")
        sys.exit(2)
