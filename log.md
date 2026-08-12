---
type: log
---

# Log

Append-only, newest at the bottom. Every entry starts with `## [date] op | title`
so the history stays greppable:

```
grep "^## \[" log.md | tail -5
```

---

## [2026-08-11] refactor | Vault initialized as an LLM wiki

Instantiated Karpathy's LLM wiki pattern in an empty vault. Created `CLAUDE.md`
(schema), `raw/`, `wiki/`, `index.md`, `log.md`, `tools/wiki-search.sh`. Set
Obsidian's attachment folder to `raw/assets/`.

## [2026-08-11] ingest | LLM Wiki — Andrej Karpathy

First source: the gist that defines the pattern, saved to
`raw/llm-wiki-karpathy.md`. Bootstrap ingest, done without prior discussion since
it is the vault's own spec.

Pages created (4): [[LLM Wiki (Karpathy)]] (source), [[Compounding Knowledge]]
(concept), [[Memex]] (concept), [[Andrej Karpathy]] (entity).
Index updated. [[Andrej Karpathy]] is thin — flagged on the page.

## [2026-08-11] refactor | Added writing/ alongside the wiki

Vault is now writing + wiki, with inverted ownership between the two halves: the
agent owns `wiki/`, the human owns every sentence in `writing/`. Enforced
mechanically by "the line" — a `---` rule per piece, above which the agent never
writes, below which is its workbench for research and cuts.

Created `writing/`, `writing/README.md`, `writing/STYLE.md` (empty scaffold —
human fills it in). Rewrote `CLAUDE.md`: new `essay` type with a
seed/draft/published/shelved status, three new operations (research, edit,
publish), two new lint checks, new log ops, and a hard rule against originating
prose. Publish includes a harvest step so finished essays pay arguments back into
the wiki. `index.md` gained a Writing section.

## [2026-08-12] ingest | The Manipulated Man — Esther Vilar

Second source, and the vault's first outside knowledge management: a 1971 polemic
inverting the feminist thesis. 69pp PDF, read in full (installed poppler to do it).

Pages created (5): [[The Manipulated Man (Vilar)]] (source), [[Esther Vilar]]
(entity), [[Male Disposability]] (concept), [[Unfalsifiable Inversion]] (concept),
[[Vilar contra Second-Wave Feminism]] (synthesis). Index updated.

Treated the book as split into two layers: a checkable empirical catalogue
(→ [[Male Disposability]]) and an unfalsifiable psychology (→ [[Unfalsifiable
Inversion]]), which is also the bridge to this vault's existing epistemics via
[[Compounding Knowledge]]. Provenance is near-zero — three unattributed statistics
in 42,000 words — so most claims carry `> [!warning] Unsourced`.

Open: [[Esther Vilar]] is thin and self-reported; publication history and the
Schwarzer debate were deliberately left out rather than asserted. The Farrell
lineage on [[Male Disposability]] is flagged as unsourced general knowledge.

## [2026-08-12] refactor | Ingest is now a single pass

Dropped the discuss-before-writing gate from the Ingest op in `CLAUDE.md`. Ingest
now runs end to end and reports afterward — takeaways, judgment calls, and open
gaps — so steering happens against real pages instead of a proposal. Added an
explicit rule that uncertainty gets filed with a warning callout rather than
stalling the ingest.

## [2026-08-12] refactor | Binary sources are now searchable

Added `extracted/` — plain-text renderings of every non-text file in `raw/`, so
PDFs and office documents stop being opaque to ripgrep. Agent-owned and derived;
`raw/` stays read-only, which is why the mirror exists at all.

New `tools/extract.sh` dispatches by extension (pdftotext for PDF, macOS textutil
for doc/docx/odt/rtf/html, pandoc for epub, tesseract for images), is idempotent,
and reports rather than silently skipping unknown formats or missing tools.
`tools/wiki-search.sh` gained `-s` for sources and now globs all file types under
`-s`/`-a`. Backfilled the Vilar PDF: 42,512 words. Schema, layout, ingest step 1,
and hard rule 1 updated to match.
