#!/usr/bin/env python3
"""Check the vault against Open Knowledge Format v0.2 and against CLAUDE.md.

Reports, never fixes — same contract as the Lint operation. Exits 1 if any ERROR
is found, 0 otherwise; warnings never fail the run.

    tools/okf-lint.py        full report
    tools/okf-lint.py -q     errors only

No dependencies beyond python3: the frontmatter parser below handles the YAML
subset this vault actually uses (scalars, flow mappings, flow sequences, and
block lists of mappings), which is why PyYAML is not required.
"""
import os
import re
import sys
from urllib.parse import unquote

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESERVED = {"index.md", "log.md"}
# raw/ is the immutable source layer, exempt by CLAUDE.md hard rule 1.
SKIP_DIRS = {".git", ".obsidian", ".claudian", "raw", "tools"}

WIKI_TYPES = {"source", "entity", "concept", "synthesis"}
META_TYPES = {"schema", "readme", "config"}
KNOWN_TYPES = WIKI_TYPES | META_TYPES | {"essay"}
OKF_STATUS = {"draft", "stable", "deprecated"}
ESSAY_STATUS = {"seed", "draft", "published", "shelved"}
LOG_OPS = {"Ingest", "Query", "Research", "Edit", "Publish", "Lint", "Refactor"}

ACTOR = re.compile(r"^(human|process|team):[a-z0-9][a-z0-9._-]*$|"
                   r"^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(T[\d:]+(\.\d+)?(Z|[+-]\d{2}:\d{2})?)?$")

errors, warnings = [], []


def err(path, msg):
    errors.append((path, msg))


def warn(path, msg):
    warnings.append((path, msg))


# --- minimal YAML subset ------------------------------------------------------

def scalar(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return s


def split_commas(s):
    parts, depth, quote, cur = [], 0, None, ""
    for ch in s:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def flow(s):
    s = s.strip()
    if s.startswith("{"):
        out = {}
        for part in split_commas(s[1:-1]):
            if ":" in part:
                k, v = part.split(":", 1)
                out[k.strip()] = scalar(v)
        return out
    if s.startswith("["):
        return [scalar(p) for p in split_commas(s[1:-1])]
    return scalar(s)


KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_.]*):\s*(.*)$")


def parse_frontmatter(text):
    """Return (dict, error_message). dict is None when no block is present."""
    if not text.startswith("---\n"):
        return None, "no YAML frontmatter block"
    end = text.find("\n---\n", 3)
    if end == -1:
        return None, "frontmatter block is never closed"
    out, key, items, cur = {}, None, None, None
    for raw_line in text[4:end + 1].splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0:
            if items is not None:
                out[key] = items
                items, cur = None, None
            m = KEY.match(stripped)
            if not m:
                return None, "unparseable line: %s" % stripped
            key, val = m.group(1), m.group(2).strip()
            if val:
                out[key] = flow(val)
                key = None
            else:
                items = []
        elif stripped.startswith("- "):
            if items is None:
                return None, "list item outside a list: %s" % stripped
            cur = {}
            items.append(cur)
            m = KEY.match(stripped[2:])
            if m:
                cur[m.group(1)] = flow(m.group(2))
            else:
                items[-1] = scalar(stripped[2:])
                cur = None
        elif cur is not None:
            m = KEY.match(stripped)
            if m:
                cur[m.group(1)] = flow(m.group(2))
    if items is not None:
        out[key] = items
    return out, None


# --- checks -------------------------------------------------------------------

def concept_files():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in sorted(files):
            if not name.endswith(".md") or name in RESERVED:
                continue
            path = os.path.join(root, name)
            if os.path.islink(path):
                continue
            yield os.path.relpath(path, VAULT)


def check_concept(rel, fm, body):
    ptype = fm.get("type")
    if not ptype:                                          # OKF §11.2
        err(rel, "missing or empty `type` (OKF conformance rule 2)")
    elif ptype not in KNOWN_TYPES:
        warn(rel, "unknown type `%s` — OKF allows it, CLAUDE.md does not list it" % ptype)

    for field in ("title", "description"):
        if not fm.get(field):
            err(rel, "missing `%s`" % field)

    status = fm.get("status")
    vocab = ESSAY_STATUS if ptype == "essay" else OKF_STATUS
    if status and status not in vocab:
        err(rel, "status `%s` outside vocabulary %s" % (status, sorted(vocab)))

    gen = fm.get("generated")
    if not isinstance(gen, dict):
        err(rel, "missing `generated: { by, at }`")
    else:
        if not ACTOR.match(str(gen.get("by", ""))):
            err(rel, "generated.by `%s` is not an actor (OKF §7)" % gen.get("by"))
        if gen.get("at") and not DATE.match(str(gen["at"])):
            err(rel, "generated.at `%s` is not an ISO 8601 date" % gen["at"])

    ver = fm.get("verified")
    for entry in ([ver] if isinstance(ver, dict) else ver or []):   # §5.2 bare mapping
        if not ACTOR.match(str(entry.get("by", ""))):
            err(rel, "verified.by `%s` is not an actor (OKF §7)" % entry.get("by"))
        if not DATE.match(str(entry.get("at", ""))):
            err(rel, "verified entry needs an ISO 8601 `at`")

    for field in ("created", "stale_after"):
        if fm.get(field) and not DATE.match(str(fm[field])):
            err(rel, "%s `%s` is not an ISO 8601 date" % (field, fm[field]))

    if fm.get("resource"):
        check_path(rel, "resource", fm["resource"])

    srcs = fm.get("sources")
    if ptype in WIKI_TYPES and not srcs:
        err(rel, "wiki page has no `sources` — provenance is the point (OKF §5.1)")
    seen = set()
    for i, s in enumerate(srcs or []):
        if not isinstance(s, dict):
            err(rel, "sources[%d] is not a mapping" % i)
            continue
        if not s.get("resource"):
            err(rel, "sources[%d] missing required `resource` (OKF §5.1)" % i)
        else:
            check_path(rel, "sources[%d].resource" % i, s["resource"])
        sid = s.get("id")
        if not sid:
            warn(rel, "sources[%d] has no `id`, so claims cannot be attributed to it" % i)
        elif sid in seen:
            err(rel, "duplicate source id `%s`" % sid)
        else:
            seen.add(sid)
        if s.get("author") and not ACTOR.match(str(s["author"])):
            err(rel, "sources[%d].author `%s` is not an actor (OKF §7)" % (i, s["author"]))
        if s.get("last_modified") and not DATE.match(str(s["last_modified"])):
            err(rel, "sources[%d].last_modified is not an ISO 8601 date" % i)

    if fm.get("title") and rel.startswith("wiki/"):
        stem = os.path.basename(rel)[:-3]
        if fm["title"] != stem:
            err(rel, "title `%s` does not match filename `%s`" % (fm["title"], stem))


def check_path(rel, field, value):
    value = str(value)
    if value.startswith(("http://", "https://")):
        return
    if not os.path.exists(os.path.join(VAULT, value.lstrip("/"))):
        err(rel, "%s points at a missing file: %s" % (field, value))


INDEX_ENTRY = re.compile(r"^\* \[([^\]]+)\]\(([^)]+)\)\s+-\s+(.*)$")
TRAILING_MARK = re.compile(r"\s*\*\([^)]*\)\*\s*$")


def check_index(pages):
    rel = "index.md"
    path = os.path.join(VAULT, rel)
    text = open(path, encoding="utf-8").read()
    fm, _ = parse_frontmatter(text)
    if fm is None:
        warn(rel, "no `okf_version` declared (OKF §12)")
    else:
        extra = set(fm) - {"okf_version"}
        if extra:                                          # OKF §8
            err(rel, "index.md may only carry `okf_version`, found: %s" % sorted(extra))
        if fm.get("okf_version") != "0.2":
            warn(rel, "okf_version is `%s`, expected 0.2" % fm.get("okf_version"))

    if not re.search(r"^#{1,2} \S", text, re.M):
        err(rel, "no section headings (OKF §8)")

    listed = {}
    for line in text.splitlines():
        m = INDEX_ENTRY.match(line.strip())
        if not m:
            continue
        title, target, desc = m.group(1), unquote(m.group(2)), m.group(3).strip()
        if not os.path.exists(os.path.join(VAULT, target)):
            err(rel, "entry `%s` links to a missing file: %s" % (title, target))
        if target.startswith("wiki/"):
            listed[target] = (title, TRAILING_MARK.sub("", desc))

    for wiki_rel, fm_page in pages.items():
        if wiki_rel not in listed:
            err(rel, "%s is not listed (hard rule 4)" % wiki_rel)
            continue
        title, desc = listed[wiki_rel]
        if fm_page.get("description") and desc != fm_page["description"].strip():
            err(rel, "description for `%s` differs from the page's frontmatter" % title)
    return listed


LOG_DATE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")
LOG_ENTRY = re.compile(r"^\* \*\*([A-Za-z]+)\*\*:")


def check_log():
    rel = "log.md"
    text = open(os.path.join(VAULT, rel), encoding="utf-8").read()
    if text.startswith("---\n"):
        err(rel, "log.md is a reserved file and should carry no frontmatter")
    dates = [m.group(1) for m in (LOG_DATE.match(l) for l in text.splitlines()) if m]
    if not dates:
        err(rel, "no `## YYYY-MM-DD` date headings (OKF §9)")
    if dates != sorted(dates, reverse=True):
        err(rel, "date headings are not newest-first (OKF §9)")
    if len(set(dates)) != len(dates):
        err(rel, "duplicate date headings")
    entries = 0
    for line in text.splitlines():
        m = LOG_ENTRY.match(line)
        if m:
            entries += 1
            if m.group(1) not in LOG_OPS:
                warn(rel, "unknown op label `%s`" % m.group(1))
    if not entries:
        err(rel, "no `* **Op**:` entries")


WIKILINK = re.compile(r"\[\[([^\]|#\n]+)")
SPLIT_WIKILINK = re.compile(r"\[\[[^\]\n]*\n[^\]]*\]\]")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text):
    """Placeholders like `[[Page Name]]` in prose about wikilinks are not links."""
    return INLINE_CODE.sub("", FENCE.sub("", text))


def check_links(bodies, listed):
    inbound = {rel: 0 for rel in bodies if rel.startswith("wiki/")}
    for rel, raw_body in bodies.items():
        # CLAUDE.md and the READMEs are documentation about wikilinks, not users
        # of them; their examples are deliberately unresolvable.
        if not rel.startswith(("wiki/", "writing/")):
            continue
        body = strip_code(raw_body)
        for hit in SPLIT_WIKILINK.findall(body):
            warn(rel, "wikilink split across lines, so Obsidian will not resolve "
                      "it: %s" % " ".join(hit.split()))
        for target in set(WIKILINK.findall(body)):
            target = target.strip()
            candidates = ["wiki/%s.md" % target, target, "%s.md" % target]
            hit = next((c for c in candidates
                        if os.path.exists(os.path.join(VAULT, c))), None)
            if hit is None:
                warn(rel, "broken wikilink: [[%s]]" % target)
            elif hit in inbound and hit != rel:
                inbound[hit] += 1
    for wiki_rel, count in sorted(inbound.items()):
        if count == 0 and wiki_rel not in listed:
            warn(wiki_rel, "orphan: no inbound links from anywhere")
        elif count == 0:
            warn(wiki_rel, "no inbound wikilinks — only reachable from index.md")


def main():
    quiet = "-q" in sys.argv
    pages, bodies = {}, {}
    checked = 0
    for rel in concept_files():
        checked += 1
        text = open(os.path.join(VAULT, rel), encoding="utf-8").read()
        fm, problem = parse_frontmatter(text)
        if fm is None:
            err(rel, problem + " (OKF conformance rule 1)")
            continue
        body = text[text.find("\n---\n", 3) + 5:]
        bodies[rel] = body
        check_concept(rel, fm, body)
        if rel.startswith("wiki/"):
            pages[rel] = fm

    listed = check_index(pages)
    check_log()
    check_links(bodies, listed)

    for path, msg in errors:
        print("ERROR  %s: %s" % (path, msg))
    if not quiet:
        for path, msg in warnings:
            print("WARN   %s: %s" % (path, msg))
        print()
        print("%d concept files checked, %d wiki pages indexed" % (checked, len(pages)))
    print("%d error%s, %d warning%s" % (len(errors), "" if len(errors) == 1 else "s",
                                        len(warnings), "" if len(warnings) == 1 else "s"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
