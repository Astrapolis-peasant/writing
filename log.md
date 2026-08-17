# Log

Newest first, grouped by ISO date, per [OKF §9](wiki/Open%20Knowledge%20Format.md).
Entries are never rewritten or deleted — new ones go on top. Every entry opens with
a bold op label so the history stays greppable:

```
grep '^\* \*\*' log.md | head -5
```

Op is one of `Ingest`, `Query`, `Research`, `Edit`, `Publish`, `Lint`, `Refactor`.

## 2026-08-17

* **Refactor**: Adopted [Open Knowledge Format](wiki/Open%20Knowledge%20Format.md)
  v0.2 as the vault's on-disk format.

  Frontmatter across all 17 wiki pages now carries OKF's provenance, trust, and
  lifecycle families. The old `sources: 1` count — which recorded nothing — becomes
  a real `sources` list naming each raw file, its author in the actor convention,
  and its publication year. `updated:` is absorbed into `generated: { by, at }`,
  which says *who* regenerated a page as well as when: `claude-code/claude-opus-5`
  for `wiki/`, `human:bonan` for `writing/`. Every page also gained `title`,
  `description`, and a `status`; source pages gained `resource`.

  `index.md` converts to OKF §8 grouped link lists, its descriptions taken verbatim
  from each page's `description` field, and drops all frontmatter but `okf_version`.
  This log converts to §9: date groups, bold op labels, newest first. Append-only
  survives as the discipline — past entries were re-indented, never rewritten.

  `verified:` was deliberately left off every page. OKF derives its human-reviewed
  trust tier from a `human:` actor in that field, so writing one in would assert a
  review that has not happened. The whole bundle sits at the unverified tier, which
  is accurate.

  New `tools/okf-lint.py` checks the three conformance rules plus vault-specific
  invariants: `sources[].resource` paths that exist, actor strings in convention,
  and index descriptions that match their pages. Deviations from OKF are documented
  in `CLAUDE.md` rather than silently taken — chiefly `[[wikilinks]]` in prose,
  which OKF never requires and Obsidian's graph depends on.

* **Ingest**: [Open Knowledge Format](wiki/Open%20Knowledge%20Format.md) —
  fourth source, saved to `raw/okf-spec-v0.2.md`.

  The spec that motivated the refactor above, filed as a source so the format
  decisions stay traceable to the document that argued for them. Cross-linked from
  [[LLM Wiki (Karpathy)]]: OKF reserves `index.md` and `log.md` with the same
  meanings Karpathy gives them, arrived at independently.

  Not propagated further. OKF bears on this vault's plumbing, not on anything the
  other fourteen pages are about.

## 2026-08-12

* **Query**: What the three commitments have in common.

  Revised [[LaVeyan Satanism]]. The three targets — Christianity, white witchcraft,
  Eastern mysticism — receive one charge, and it is insincerity rather than falsity:
  LaVey argues nowhere that these beliefs are untrue, only that nobody holds them.
  That leaves the book without an argument against any of the positions, and with no
  room for a sincere opponent, which is the same closure recorded in
  [[Unfalsifiable Inversion]].

  Also noted on [[The Satanic Bible (LaVey)]]: the Underground Edition's extras
  include LaVey prose in the first person plural that the Book of Lucifer rewrites in
  the third — plausibly one of the precursor monographs, printed alongside the text
  it became. Marked *(inferred)*; the passage is untitled in the contents.

* **Ingest**: The Satanic Bible — Anton LaVey.

  Third source, first run of the single-pass ingest. 146pp, 65,563 words, extracted
  automatically by `tools/extract.sh` and read in full.

  Pages created (6): [[The Satanic Bible (LaVey)]] (source), [[Anton LaVey]] and
  [[Church of Satan]] (entities), [[LaVeyan Satanism]], [[Ritual as Psychodrama]] and
  [[Psychic Vampire]] (concepts), plus [[The Sources of the Satanic Bible]]
  (synthesis). Index updated.

  Propagated to [[Unfalsifiable Inversion]], which now carries LaVey as a second and
  cleaner specimen — his theory of curses converts skepticism into confirmation
  explicitly. That page is the first in the vault to reach two sources.

  The find of the ingest: this "Underground Edition" bundles Temple of Set appendices
  that print Ragnar Redbeard's *Might Is Right* (1896) beside the Book of Satan,
  showing it to be near-verbatim, and map the Nine Satanic Statements onto Galt's
  speech in *Atlas Shrugged*. LaVey cut Redbeard's racial-extermination material. The
  Church of Satan's own 2005 introduction concedes the sourcing.

  Open: everything on [[Anton LaVey]] and [[Church of Satan]] is self-reported or
  comes from schismatics — no independent source yet. Reception, membership figures,
  and the 1975 schism's causes are unestablished.

* **Refactor**: Binary sources are now searchable.

  Added `extracted/` — plain-text renderings of every non-text file in `raw/`, so
  PDFs and office documents stop being opaque to ripgrep. Agent-owned and derived;
  `raw/` stays read-only, which is why the mirror exists at all.

  New `tools/extract.sh` dispatches by extension (pdftotext for PDF, macOS textutil
  for doc/docx/odt/rtf/html, pandoc for epub, tesseract for images), is idempotent,
  and reports rather than silently skipping unknown formats or missing tools.
  `tools/wiki-search.sh` gained `-s` for sources and now globs all file types under
  `-s`/`-a`. Backfilled the Vilar PDF: 42,512 words. Schema, layout, ingest step 1,
  and hard rule 1 updated to match.

* **Refactor**: Ingest is now a single pass.

  Dropped the discuss-before-writing gate from the Ingest op in `CLAUDE.md`. Ingest
  now runs end to end and reports afterward — takeaways, judgment calls, and open
  gaps — so steering happens against real pages instead of a proposal. Added an
  explicit rule that uncertainty gets filed with a warning callout rather than
  stalling the ingest.

* **Ingest**: The Manipulated Man — Esther Vilar.

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

## 2026-08-11

* **Refactor**: Added `writing/` alongside the wiki.

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

* **Ingest**: LLM Wiki — Andrej Karpathy.

  First source: the gist that defines the pattern, saved to
  `raw/llm-wiki-karpathy.md`. Bootstrap ingest, done without prior discussion since
  it is the vault's own spec.

  Pages created (4): [[LLM Wiki (Karpathy)]] (source), [[Compounding Knowledge]]
  (concept), [[Memex]] (concept), [[Andrej Karpathy]] (entity).
  Index updated. [[Andrej Karpathy]] is thin — flagged on the page.

* **Refactor**: Vault initialized as an LLM wiki.

  Instantiated Karpathy's LLM wiki pattern in an empty vault. Created `CLAUDE.md`
  (schema), `raw/`, `wiki/`, `index.md`, `log.md`, `tools/wiki-search.sh`. Set
  Obsidian's attachment folder to `raw/assets/`.
