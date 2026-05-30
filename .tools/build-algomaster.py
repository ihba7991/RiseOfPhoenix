#!/usr/bin/env python3
"""
Build the per-person AlgoMaster tracker.

Takes the source ~/Downloads/algomaster-leetcode.html, augments it with
checkbox + notes-link UI and localStorage persistence, and emits a
companion algomaster-notes.md with stable anchors per problem.

Writes both files into each person's competitive-programming/ folder.

Run from the repo root.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SRC = Path.home() / "Downloads" / "algomaster-leetcode.html"
PEOPLE = ["ihba7991", "vikku"]


def extract_data(html: str) -> list[dict]:
    """Pull the JSON array assigned to `const DATA = [...]` and parse it."""
    m = re.search(r"const DATA = (\[.*?\]);\n", html, re.DOTALL)
    if not m:
        raise SystemExit("could not locate `const DATA = [...];` in source HTML")
    return json.loads(m.group(1))


def assign_ids(data: list[dict]) -> list[dict]:
    """Mutate items to add stable `id` fields: p-NNN / c-NNN counted globally."""
    pn = cn = 0
    for section in data:
        for item in section["items"]:
            if item["type"] == "problem":
                pn += 1
                item["id"] = f"p-{pn:03d}"
            else:
                cn += 1
                item["id"] = f"c-{cn:03d}"
    return data


def render_notes_md(data: list[dict]) -> str:
    """One markdown file with anchored sections per problem (concepts skipped)."""
    lines: list[str] = []
    lines.append("# AlgoMaster — Notes & Learning")
    lines.append("")
    lines.append(
        "Companion notes for every problem in [`algomaster-leetcode.html`](./algomaster-leetcode.html). "
        "Each problem has a stable anchor (`p-NNN`) so the tracker's *Notes* link drops you directly "
        "to its section. Write what stuck — pattern, trick, edge case, time."
    )
    lines.append("")
    lines.append("**How to use**")
    lines.append("")
    lines.append("- The tracker links to `#p-001`, `#p-002`, …")
    lines.append("- Add your notes under the heading; commit when you push solutions.")
    lines.append("- Keep notes terse: pattern · key insight · pitfall · TC/SC.")
    lines.append("")

    for section in data:
        problem_items = [it for it in section["items"] if it["type"] == "problem"]
        if not problem_items:
            continue
        lines.append(f"## §{section['n']:02d}. {section['name']}")
        lines.append("")
        for item in problem_items:
            anchor_id = item["id"]
            diff = item.get("diff", "Problem")
            badge = f"`{diff}`"
            title = item["title"]
            algo = item.get("algo", "")
            leet = item.get("leet", "")
            links = []
            if algo:
                links.append(f"[AlgoMaster]({algo})")
            if leet:
                links.append(f"[LeetCode]({leet})")
            links_str = " · ".join(links)
            lines.append(f'<a id="{anchor_id}"></a>')
            lines.append(f"### {anchor_id} · {title} {badge}")
            if links_str:
                lines.append("")
                lines.append(links_str)
            lines.append("")
            lines.append("_Your notes…_")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# HTML augmentation
# ---------------------------------------------------------------------------

# Extra CSS injected before </style>
EXTRA_CSS = r"""
/* tracker additions */
.cb{width:18px;height:18px;border:1.4px solid var(--line);border-radius:5px;flex:none;
  display:inline-flex;align-items:center;justify-content:center;font:600 11px var(--mono);
  color:transparent;cursor:pointer;background:var(--bg);transition:.12s}
.cb:hover{border-color:var(--acc2)}
.cb.on{background:rgba(126,231,135,.16);border-color:var(--acc2);color:var(--acc2)}
.cb-spacer{display:inline-block;width:18px;height:18px;flex:none}
.row.done .name .t{text-decoration:line-through;color:var(--mut)}
.row.done{opacity:.55}
.lk.note{color:var(--acc2);border-color:rgba(126,231,135,.3)}
.lk.note:hover{color:var(--acc2);border-color:var(--acc2)}
.stat.d .v{color:var(--acc2)}
.backlink{display:block;padding:8px 12px;margin:4px 0 14px;border:1px solid var(--line);
  border-radius:8px;font:600 12px var(--mono);letter-spacing:.05em;color:var(--mut);
  background:var(--panel)}
.backlink:hover{color:var(--acc);border-color:var(--acc)}
"""

# New render script — replaces everything between the opening `<script>` and `</script>`
# that contains the original render JS. Preserves `const DATA = …;` as-is.
NEW_RENDER_JS = r"""
let curDiff = "All", curQ = "";
const STORAGE_KEY = 'am-done';
function loadDone(){
  try{ return new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')); }
  catch(_){ return new Set(); }
}
function saveDone(s){ try{ localStorage.setItem(STORAGE_KEY, JSON.stringify([...s])); }catch(_){ } }
const done = loadDone();

// build sidebar nav
const nav = document.getElementById('nav');
let nh = '<a class="backlink" href="../../index.html">&larr; Dashboard</a>';
nh += '<h2>Sections</h2>';
DATA.forEach(s=>{
  const pc = s.items.filter(i=>i.type==='problem').length;
  nh += `<div class="navlink" onclick="document.getElementById('sec${s.n}').scrollIntoView()">
    <span>${s.name}</span><b>${pc||''}</b></div>`;
});
nav.innerHTML = nh;

const allP = DATA.flatMap(s=>s.items).filter(i=>i.type==='problem');
function paintStats(){
  const c={Easy:0,Medium:0,Hard:0};
  allP.forEach(p=>c[p.diff]++);
  const dn = allP.filter(p=>done.has(p.id)).length;
  document.getElementById('stats').innerHTML =
    `<div class="stat"><div class="v">${allP.length}</div><div class="l">Problems</div></div>
     <div class="stat e"><div class="v">${c.Easy}</div><div class="l">Easy</div></div>
     <div class="stat m"><div class="v">${c.Medium}</div><div class="l">Medium</div></div>
     <div class="stat h"><div class="v">${c.Hard}</div><div class="l">Hard</div></div>
     <div class="stat d"><div class="v">${dn}</div><div class="l">Done</div></div>
     <div class="stat"><div class="v">${DATA.length}</div><div class="l">Sections</div></div>`;
}
paintStats();

function esc(s){return s.replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]))}

function rowHtml(it){
  // Concepts are pure lessons — no checkbox, no notes link.
  if(it.type==='concept'){
    return `<div class="row" data-id="${it.id}">
      <span class="cb-spacer"></span>
      <span class="dot concept"></span>
      <div class="name concept"><span class="t">${esc(it.title)}</span></div>
      <span class="badge lesson">Lesson</span>
      <div class="links">
        <a class="lk algo" href="${it.algo}" target="_blank" rel="noopener">AlgoMaster</a>
      </div></div>`;
  }
  const isDone = done.has(it.id);
  const cb = `<span class="cb ${isDone?'on':''}" data-id="${it.id}" role="checkbox" aria-checked="${isDone}" title="Mark done">${isDone?'✓':''}</span>`;
  const note = `<a class="lk note" href="./algomaster-notes.md#${it.id}" target="_blank" rel="noopener">Notes</a>`;
  const lc = it.search
    ? `<a class="lk leet search" href="${it.leet}" target="_blank" rel="noopener" title="No exact LeetCode match — opens search">LeetCode &#8599;</a>`
    : `<a class="lk leet" href="${it.leet}" target="_blank" rel="noopener">LeetCode</a>`;
  return `<div class="row ${isDone?'done':''}" data-id="${it.id}">
    ${cb}
    <span class="dot ${it.diff}"></span>
    <div class="name"><span class="t">${esc(it.title)}</span></div>
    <span class="badge ${it.diff}">${it.diff}</span>
    <div class="links">
      <a class="lk algo" href="${it.algo}" target="_blank" rel="noopener">AlgoMaster</a>
      ${lc}
      ${note}
    </div></div>`;
}

function render(){
  const q = curQ.trim().toLowerCase();
  const list = document.getElementById('list');
  let out = '', shown = 0;
  DATA.forEach(s=>{
    let rows = '', lastSub = null, secCount = 0;
    s.items.forEach(it=>{
      if(it.type==='problem'){
        if(curDiff!=='All' && it.diff!==curDiff) return;
        if(q && !it.title.toLowerCase().includes(q) && !s.name.toLowerCase().includes(q)) return;
      } else {
        if(curDiff!=='All') return;
        if(q && !it.title.toLowerCase().includes(q) && !s.name.toLowerCase().includes(q)) return;
      }
      if(it.sub && it.sub!==lastSub){ rows += `<div class="subhead">${esc(it.sub)}</div>`; lastSub = it.sub; }
      else if(!it.sub) lastSub = null;
      secCount++; shown++;
      rows += rowHtml(it);
    });
    if(rows){
      out += `<section class="sec" id="sec${s.n}"><div class="sechead">
        <span class="no">${String(s.n).padStart(2,'0')}</span><h3>${esc(s.name)}</h3>
        <span class="ct">${secCount} shown</span></div>${rows}</section>`;
    }
  });
  list.innerHTML = out;
  document.getElementById('empty').style.display = shown? 'none':'block';
}

document.getElementById('q').addEventListener('input',e=>{curQ=e.target.value;render()});
document.getElementById('filters').addEventListener('click',e=>{
  const b=e.target.closest('.chip'); if(!b)return;
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('on'));
  b.classList.add('on'); curDiff=b.dataset.d; render();
});

// Single delegated click handler for checkbox toggles
document.getElementById('list').addEventListener('click', e => {
  const cb = e.target.closest('.cb');
  if(!cb) return;
  e.preventDefault();
  const id = cb.dataset.id;
  if(done.has(id)) done.delete(id); else done.add(id);
  saveDone(done);
  paintStats();
  // Toggle row visual cheaply without full re-render
  const row = cb.closest('.row');
  const nowDone = done.has(id);
  row.classList.toggle('done', nowDone);
  cb.classList.toggle('on', nowDone);
  cb.textContent = nowDone ? '✓' : '';
  cb.setAttribute('aria-checked', nowDone);
});

render();
"""

def patch_html(src_html: str, data: list[dict]) -> str:
    """Return modified HTML with augmented CSS + new render JS + back link."""

    # 1) Inject extra CSS just before </style>
    html = src_html.replace("</style>", EXTRA_CSS + "</style>", 1)

    # 3) Replace DATA with the id-augmented version (so notes anchors work).
    new_data_literal = "const DATA = " + json.dumps(data, separators=(", ", ": ")) + ";\n"

    # 4) Replace the entire script that lives between `<script>\nconst DATA = ` …
    # and the closing `</script>` before `</body>` — with new DATA + new render JS.
    pattern = re.compile(r"<script>\s*const DATA = .*?</script>", re.DOTALL)
    replacement = "<script>\n" + new_data_literal + NEW_RENDER_JS + "</script>"
    # Pass replacement via a lambda so it's used literally — JSON contains
    # backslash escapes (e.g. \uXXXX) that re.sub() would otherwise interpret.
    new_html, n = pattern.subn(lambda _m: replacement, html, count=1)
    if n != 1:
        raise SystemExit("failed to substitute <script>…</script> block")
    return new_html


def main() -> None:
    src_html = SRC.read_text(encoding="utf-8")
    data = assign_ids(extract_data(src_html))
    patched_html = patch_html(src_html, data)
    notes_md = render_notes_md(data)

    repo_root = Path(__file__).resolve().parent.parent
    for who in PEOPLE:
        target_dir = repo_root / who / "competitive-programming"
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "algomaster-leetcode.html").write_text(patched_html, encoding="utf-8")
        (target_dir / "algomaster-notes.md").write_text(notes_md, encoding="utf-8")
        print(f"wrote {target_dir}/algomaster-leetcode.html")
        print(f"wrote {target_dir}/algomaster-notes.md")

    # remove .gitkeep stubs that are now obsolete
    for who in PEOPLE:
        gk = repo_root / who / "competitive-programming" / ".gitkeep"
        if gk.exists():
            gk.unlink()
            print(f"removed {gk}")


if __name__ == "__main__":
    main()
