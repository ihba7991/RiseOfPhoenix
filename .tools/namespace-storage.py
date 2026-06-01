#!/usr/bin/env python3
"""
Inject a localStorage-namespacing snippet into every per-person tracker
HTML file so progress on ihba7991/... doesn't show up on vikku/... (and
vice versa) when both sites are served from the same origin.

The snippet patches `Storage.prototype.{get,set,remove}Item` to prepend
the person's folder name (derived from `location.pathname`) to a fixed
list of known tracker keys. Other localStorage keys pass through
untouched. A one-time migration copies any existing shared values into
the person-scoped bucket so progress made before this fix isn't lost.

Idempotent: a marker comment (`<!-- riop-ns -->`) is left in each file
on first injection, and re-runs skip files that already contain it.
"""

from __future__ import annotations

from pathlib import Path

MARKER = "<!-- riop-ns -->"

# Tracker files maintained by hand (the AlgoMaster file is regenerated
# by .tools/build-algomaster.py and patched separately there).
TARGETS = [
    "ihba7991/ai/build-your-own-ai.html",
    "ihba7991/languages/build-your-own-backend-frontend.html",
    "ihba7991/lld/design-patterns.html",
    "ihba7991/lld/machine-coding.html",
    "ihba7991/lld/concurrency.html",
    "vikku/ai/build-your-own-ai.html",
    "vikku/languages/build-your-own-backend-frontend.html",
    "vikku/lld/design-patterns.html",
    "vikku/lld/machine-coding.html",
    "vikku/lld/concurrency.html",
]

NS_SNIPPET = MARKER + """
<script>
/*
 * Per-person localStorage namespacing.
 *
 * The trackers live at /<person>/<...>/<file>.html on a shared origin,
 * so without this every tracker key (e.g. 'am-done', 'dp-done') would
 * be shared across people. We rewrite getItem/setItem/removeItem to
 * prefix the person's folder name when it sees one of our known keys.
 */
(function () {
  var PEOPLE  = ['ihba7991', 'vikku'];
  var PERSON  = (location.pathname.split('/').filter(Boolean)
                 .find(function (s) { return PEOPLE.indexOf(s) !== -1; })) || 'default';
  var NS_KEYS = ['byodone', 'byo-be-done', 'byo-fafo-done',
                 'dp-done', 'mc-done', 'cc-done', 'am-done'];
  function ns(k) { return NS_KEYS.indexOf(k) !== -1 ? (PERSON + ':' + k) : k; }

  var proto = Storage.prototype;
  var oGet  = proto.getItem;
  var oSet  = proto.setItem;
  var oDel  = proto.removeItem;
  proto.getItem    = function (k)    { return oGet.call(this, ns(k)); };
  proto.setItem    = function (k, v) { return oSet.call(this, ns(k), v); };
  proto.removeItem = function (k)    { return oDel.call(this, ns(k)); };

  // One-time migration: any shared-key values become the person's values.
  try {
    NS_KEYS.forEach(function (k) {
      var personKey = PERSON + ':' + k;
      if (oGet.call(localStorage, personKey) === null) {
        var legacy = oGet.call(localStorage, k);
        if (legacy !== null) oSet.call(localStorage, personKey, legacy);
      }
    });
  } catch (_) { /* private mode / quota issues — ignore */ }
})();
</script>
"""


def patch(path: Path) -> bool:
    """Inject the snippet right after <body>. Idempotent. Returns True if changed."""
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    if "<body>" not in text:
        raise SystemExit(f"no <body> tag found in {path}")
    text = text.replace("<body>", "<body>\n" + NS_SNIPPET, 1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    changed = 0
    for rel in TARGETS:
        p = repo_root / rel
        if not p.exists():
            print(f"skipped (missing): {rel}")
            continue
        if patch(p):
            changed += 1
            print(f"patched: {rel}")
        else:
            print(f"unchanged: {rel}")
    print(f"{changed} file(s) patched.")


if __name__ == "__main__":
    main()
