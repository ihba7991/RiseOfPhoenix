# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A shared learning tracker for two collaborators (`ihba7991` and `vikku`). The user-facing artifact is a GitHub Pages site at `https://ihba7991.github.io/RiseOfPhoenix/` that auto-deploys from `main`. Each collaborator has a folder of self-contained HTML trackers (DSA, LLD, AI/ML, web stack) whose checkbox state persists to `localStorage`. The site's landing dashboard renders a recent-commits feed plus links into each person's trackers.

This is **not a typical app codebase** — there is no framework, no bundler, no test suite. The "logic" is a handful of static HTML files plus four small Python/Bash scripts under `.tools/` that generate or patch them. Treat it like a small content-and-tooling project, not a webapp.

## Commands

```bash
# Regenerate the AlgoMaster tracker from ~/Downloads/algomaster-leetcode.html
# Writes <person>/competitive-programming/algomaster-{leetcode.html,notes.md}.
python3 .tools/build-algomaster.py

# Scaffold a folder + README per item under each LLD tracker
# (design-patterns, machine-coding, concurrency). Idempotent — overwrites
# READMEs, never the surrounding files.
python3 .tools/scaffold-lld.py

# Inject the localStorage-namespacing snippet into hand-authored tracker
# files. Idempotent via a `<!-- riop-ns -->` marker. Run after creating a
# new tracker HTML by hand. The AlgoMaster generator above already bakes
# the same snippet in, so do not re-run this against AlgoMaster.
python3 .tools/namespace-storage.py

# Inside any item folder under <person>/lld/<tracker>/<item>/, scaffold a
# plain-Java workspace (src/Main.java + run.sh + .gitignore). Idempotent.
bash "$(git rev-parse --show-toplevel)/.tools/init-java.sh"
./run.sh                                                  # compile + run

# Preview the deployed site locally. Mirror the GitHub Actions build step,
# then serve the assembled `_site/` (which is gitignored).
rm -rf _site && mkdir -p _site && cp -R docs/. _site/
for p in ihba7991 vikku; do mkdir -p "_site/$p"; cp -R "$p/." "_site/$p/"; done
python3 -m http.server 8765 --directory _site
```

There are no tests, no linter, no build step.

## Architecture

```
<repo root>/
├── docs/                       — dashboard, deployed at /
│   ├── index.html              — landing; reads PEOPLE + TRACKERS from inline JS
│   └── assets/dashboard.css    — single stylesheet
│
├── ihba7991/  vikku/           — per-person folders, mirrored layouts
│   ├── ai/    languages/   lld/   competitive-programming/
│   └── …each contains a tracker HTML and (for some) related .md notes
│
├── .github/workflows/pages.yml — assembles `_site/` + snapshots commits via
│                                 `gh api` + deploys with actions/deploy-pages
├── .tools/                     — see Commands above
└── ai/  hld/  lld/  …          — legacy/shared reference material, untouched
                                  by the trackers and not served
```

### Trackers and their data

Each tracker is a single self-contained HTML page (CSS + data + render JS in one file). The "data" — the list of problems, patterns, topics — is duplicated in **three** places that must stay in sync:

| Tracker | HTML data location | Other authoritative copy |
| --- | --- | --- |
| `lld/design-patterns.html` | inline `PATTERNS` literal | `.tools/scaffold-lld.py` (`DESIGN_PATTERNS`) |
| `lld/machine-coding.html`  | inline `PROBLEMS` literal | `.tools/scaffold-lld.py` (`MACHINE_CODING`) |
| `lld/concurrency.html`     | inline `TOPICS` literal   | `.tools/scaffold-lld.py` (`CONCURRENCY`) |
| `competitive-programming/algomaster-leetcode.html` | inline `const DATA` (generated) | `~/Downloads/algomaster-leetcode.html` (source) |
| `ai/build-your-own-ai.html`, `languages/build-your-own-*.html` | inline `PROJECTS` literal | external — provided as-is |

When the user asks to "add a pattern" or "add a problem," update both the HTML literal *and* the corresponding `.tools/scaffold-lld.py` entry, then re-run `scaffold-lld.py` so each item gets a folder. For AlgoMaster, edit the source file in `~/Downloads/` and re-run `build-algomaster.py`.

### localStorage namespacing (important)

All trackers live on the same origin under `/<person>/...`, so naive `localStorage.getItem('am-done')` would be shared between `ihba7991` and `vikku` pages. The fix lives at the top of every tracker HTML, right after `<body>`, marked by `<!-- riop-ns -->`:

```html
<!-- riop-ns -->
<script>
  (function () {
    var PEOPLE  = ['ihba7991', 'vikku'];
    var PERSON  = location.pathname.split('/').filter(Boolean)
                    .find(function (s) { return PEOPLE.indexOf(s) !== -1; }) || 'default';
    var NS_KEYS = ['byodone','byo-be-done','byo-fafo-done',
                   'dp-done','mc-done','cc-done','am-done'];
    // …rewrites Storage.prototype.{get,set,remove}Item for known keys
    // …plus a one-time migration of any pre-existing shared values
  })();
</script>
```

If you add a new tracker, you must also add its storage key to **two** places:
1. `NS_KEYS` in `.tools/namespace-storage.py` (the canonical list, also the snippet template) — then re-run it.
2. `NS_KEYS` in `.tools/build-algomaster.py`'s `NS_SNIPPET` — only if AlgoMaster might need to read that key (rare).

Forgetting this means progress will leak between people.

### Dashboard data flow

`docs/index.html` is fully static. At page load it tries:
1. `./commits.json` first — a build-time snapshot written by the workflow via `gh api`. Works for private repos using `GITHUB_TOKEN`. Avoids client-side API rate limits.
2. Live `https://api.github.com/repos/<owner>/<repo>/commits` as a fallback for local dev.

Per-person cards are configured by the `PEOPLE` array near the top of `docs/index.html`. If a person is renamed, update both `PEOPLE[].folder/github` *and* the workflow's hardcoded `for p in ihba7991 vikku` loop in `pages.yml`.

### Deploy

`.github/workflows/pages.yml` runs on push to `main`:
1. `cp -R docs/. _site/` + per-person mirroring.
2. `gh api repos/${{ github.repository }}/commits?per_page=30 > _site/commits.json`.
3. `actions/upload-pages-artifact` + `actions/deploy-pages`.

**One-time setup that cannot be done from CI:** repo Settings → Pages → Source: **GitHub Actions**. If pushes are succeeding but the site isn't updating, this is the first thing to check.

## Things that have bitten us

- **Re-running `build-algomaster.py` after the source HTML is updated regenerates the entire tracker including the `<!-- riop-ns -->` snippet.** Do not also run `namespace-storage.py` against the AlgoMaster file — `namespace-storage.py`'s `TARGETS` list excludes it for that reason.
- **Pushes that touch `.github/workflows/` require the `workflow` OAuth scope** on the gh CLI token. If `gh auth login` was done without it, fix with `gh auth refresh -h github.com -s workflow`.
- **Origin is HTTPS by default**; `osxkeychain` credentials weren't surfacing in non-interactive shells, so prefer `gh auth setup-git` over swapping to SSH unless the user explicitly asks.
- **`_site/` is gitignored** and rebuilt fresh for every preview. Never commit it.
- **The repo is private.** Public GitHub API calls (e.g., for commit feed) will 404 — the `commits.json` build-time snapshot is what makes the dashboard work.
- **macOS bash is 3.2** — `mapfile` and other bash 4 features are unavailable. The generated `run.sh` uses unquoted command substitution instead. Anything new should stay portable.
