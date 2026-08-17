---
type: schema
title: "Vault Schema"
description: "The conventions and workflows this vault runs on — page types, the line, operations, hard rules."
created: 2026-08-11
generated: { by: claude-code/claude-opus-5, at: 2026-08-17 }
status: stable
tags: [meta, schema]
---

# Vault Schema

This vault has two halves that feed each other:

- A **wiki** ([Karpathy's pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) —
  not a RAG index, but a persistent, compounding artifact that the agent maintains.
- **Writing** — essays and posts headed for an audience, written by the human.

The wiki is where reading gets metabolized. The writing is what it is for. A
finished essay pays back into the wiki as new pages, so the next essay starts
further along.

**Division of labor:**

| | wiki, `index.md`, `log.md` | `writing/` |
|---|---|---|
| **Human** | curates sources, directs analysis, asks questions | writes every sentence |
| **Agent** | writes and maintains all of it | researches, critiques, edits on request |

The human should rarely need to hand-edit a wiki page; if they do, the schema
needs updating. The agent must never originate prose in `writing/` — see
[Hard rules](#hard-rules).

## Layout

```
raw/            immutable sources — READ ONLY, never edit or delete
raw/assets/     images and attachments for sources
extracted/      derived plain text from raw/ — searchable, regenerable
wiki/           agent-owned markdown pages (flat, wikilinked)
writing/        human-owned essays and posts (flat)
writing/STYLE.md  voice guide — the agent reads this before any edit
index.md        catalog of every wiki page and piece, by category (OKF §8)
log.md          chronological record, newest first (OKF §9)
tools/          helper scripts
CLAUDE.md       this file — the schema
```

Both `wiki/` and `writing/` are deliberately **flat**. Obsidian resolves
`[[Page Name]]` by filename, so folders buy nothing and cost churn.
Categorization lives in `index.md` and in each page's `type` frontmatter field.

---

# Format

The vault root is an [[Open Knowledge Format]] v0.2 bundle. `index.md` declares
`okf_version: "0.2"`; `index.md` and `log.md` are OKF's two reserved filenames and
are not concept documents. Everything else with an `.md` extension is a concept and
must carry parseable YAML frontmatter with a non-empty `type` — including the
`README.md` files and this one.

Conforming costs almost nothing and buys provenance, trust, and lifecycle metadata
that the vault was expressing in prose callouts alone. Run `tools/okf-lint.py`
after any structural change.

## Deviations, taken deliberately

| Deviation | Why |
|---|---|
| `[[wikilinks]]` in page bodies, not markdown links | OKF §6 describes how to link, never requires it, and explicitly tolerates unresolvable links. Obsidian's graph, backlinks, and rename-refactoring all key off wikilinks. `index.md` uses real markdown links so a non-Obsidian consumer can still traverse the bundle. |
| `([[Source Page]])` inline attribution instead of §5.1 footnotes keyed to `sources[].id` | Page-level `sources` already carries provenance for a machine. Footnotes would degrade reading for the one human who uses this. |
| `published:` on source entries instead of `last_modified:` | OKF defines `last_modified` as the source's last change date. A 1969 print edition has none available, and inventing one violates hard rule 5. |
| Date-only `generated.at`, not a full ISO 8601 datetime | The vault works in days. A fabricated `T00:00:00Z` would assert precision that does not exist. |
| Relative paths in `index.md`, not §6.1's recommended `/`-absolute form | A leading slash breaks Obsidian's link resolution. OKF accepts both. |
| `raw/*.md` carries no frontmatter, failing §11's first conformance rule | Hard rule 1 forbids editing the source layer, and conformance would require it. `raw/` is treated as outside the concept tree — it is the material the bundle is *about*. `extracted/` holds only `.txt` and raises no question. |
| No Attested Computation concepts | Nothing here computes. |

---

# The wiki

## Page types

Every wiki page carries YAML frontmatter with a `type`:

| type | what it is | example |
|---|---|---|
| `source` | summary of one document in `raw/` | `LLM Wiki (Karpathy).md` |
| `entity` | a person, org, product, place | `Andrej Karpathy.md` |
| `concept` | an idea, mechanism, or theme | `Compounding Knowledge.md` |
| `synthesis` | cross-cutting analysis, comparison, thesis | `RAG vs Wiki.md` |

### Frontmatter

```yaml
---
type: concept                     # source | entity | concept | synthesis
title: "Unfalsifiable Inversion"  # = filename
description: "One sentence. Reused verbatim as this page's line in index.md."
created: 2026-08-12
generated: { by: claude-code/claude-opus-5, at: 2026-08-12 }
status: stable                    # draft | stable | deprecated
sources:                          # every raw source feeding the page
  - id: vilar-manipulated-man     # stable key, reused across pages
    resource: "raw/Esther-Vilar-The-Manipulated-Man.pdf"
    title: "The Manipulated Man"
    author: human:esther-vilar    # actor convention, see below
    published: 1971
tags: [argumentation, epistemics]
---
```

`source` pages add `resource:` — the raw file the page is about — and `url:` when
the original lives on the web.

**Actors** identify who did something: `<producer>/<version>` for agents
(`claude-code/claude-opus-5`), `human:<id>` for people (`human:bonan`),
`process:<id>` for automation. The prefix is load-bearing — OKF derives trust from
it, so `human:` must never be used for machine-written content.

**`generated` replaces `updated`.** It records who last regenerated the page as
well as when. Every `wiki/` page is agent-generated by definition; every piece in
`writing/` is `human:bonan`.

**`verified` is not written speculatively.** A page gets
`verified: { by: human:bonan, at: <date> }` only when the human has actually read
and confirmed it. Absent the key, OKF reads the page as unverified, which is the
honest default. Writing it in unasked would be inventing a fact about the human.

**`status`** is lifecycle, not trust: `draft` for thin or unreviewed pages,
`stable` for pages that are done as far as their sources allow, `deprecated` for
pages kept only for their links. A well-sourced page and a page whose single source
is self-reported are both `stable` — the sourcing problem belongs in `sources` and
in a `> [!warning]` callout, not here. `stale_after:` is available for claims with
a known expiry; most of this vault has none.

### Page conventions

- **Title = filename**, in natural language. No date prefixes, no slugs.
  `Andrej Karpathy.md`, not `2026-08-11-andrej-karpathy.md`.
- Open with a one-sentence definition. A reader should get the gist from line one.
- **Link generously.** First mention of any entity or concept that has (or deserves)
  a page gets a `[[wikilink]]`. Cross-references are the point of the wiki.
- **Attribute claims.** End a claim with `([[Source Page]])` so provenance survives.
  A claim with no traceable source is a liability — mark it `> [!warning] Unsourced`.
- **Flag contradictions, don't silently resolve them.** When a new source disputes an
  existing claim, keep both and mark it:
  ```
  > [!conflict] Disputed
  > [[Source A]] claims X; [[Source B]] (newer) claims Y. Unresolved.
  ```
- Prefer revising a page in place over appending. Pages should read as if written
  once, by someone who had already read everything.
- Keep pages tight — roughly 200-800 words. When a page outgrows that, it usually
  wants to be split, and the split is itself useful knowledge.
- Never let a page have zero inbound links. If nothing links to it, either link it
  from a relevant page or it should not exist.

---

# Writing

One file per piece, flat in `writing/`. Same naming rule as the wiki: the title
is the filename, in natural language.

## The line

Every piece is split by a `---` horizontal rule:

```markdown
The essay. Every sentence here is the human's.

---

## Notes
Below the line is the workbench. The agent may write here freely.
```

**Above the line, the agent does not write.** Below it — under headings the human
has created, typically `## Notes`, `## Sources`, or `## Cuts` — the agent files
research, stashes material, and parks cut paragraphs. The workbench is stripped
at publish time.

This is the whole mechanism protecting the voice. It is mechanical, so there is
never a judgment call about whether an edit went too far.

### What the agent may and may not do

| May | May not |
|---|---|
| Critique structure, argument, evidence, and pacing | Write new sentences or paragraphs above the line |
| Line-edit above the line **when explicitly asked** | Rewrite a passage into its own voice |
| Cut, and move existing sentences | Fill a `TODO` with invented text |
| Flag a claim that needs a source, and supply the `[[wikilink]]` | Change the title or thesis unasked |
| Write anything below the line | Leave research below the line if it belongs in the wiki |
| Edit frontmatter (`status`, `generated.at`, `url`, `venue`) | |

When asked for a line edit: prefer a cut to a rewrite, and never replace a
sentence that already works. Read `writing/STYLE.md` first, every time.

### Frontmatter

```yaml
---
type: essay
title: "The title, again"
description: "One sentence — what the piece argues."
status: draft           # seed | draft | published | shelved
created: 2026-08-11
generated: { by: human:bonan, at: 2026-08-11 }
venue:                  # where it is going, or where it went
url:                    # filled in on publish
tags: [knowledge-management]
---
```

`type` is `essay` for everything with an audience — posts, essays, threads.

`status` keeps the vault's own vocabulary rather than OKF's `draft | stable |
deprecated`, because the essay pipeline is not a lifecycle. An OKF consumer should
read it as: `seed`/`draft` → draft, `published` → stable, `shelved` → deprecated.

`generated.by` stays `human:bonan` on every piece, including after an agent line
edit. The prose is the human's regardless of who moved a sentence; that is the whole
point of the line.

### Conventions

- **Cite the wiki inline** with `[[wikilinks]]`. They are scaffolding for the
  writer, not the reader: convert them to real links or strip them at publish.
- A `seed` can be three lines. Do not let the status ladder become a reason not
  to start a file.
- If a piece needs a fact the wiki does not have, that is a wiki gap. Say so.

---

# Operations

## Ingest

Trigger: a new file lands in `raw/`, or the human says "ingest X".

**Run it start to finish in one pass.** Do not stop to check in before writing —
the human steers afterward, on pages that already exist.

1. If the source is not already plain text, run `tools/extract.sh` and read the
   rendering in `extracted/`. Read it **in full**. If it embeds images, read the
   text first, then view the images in `raw/assets/` separately for extra context.
2. Write a `source` page in `wiki/` summarizing it.
3. Propagate: update every existing entity/concept/synthesis page the source
   touches. A single good source often moves 10-15 pages. Do not stop at one.
4. Create new entity/concept pages for anything substantial that lacks a page.
5. Note any piece in `writing/` the source bears on — new evidence for a draft,
   or a claim it contradicts. Say it in chat; do not edit the piece.
6. Update `index.md` — a line per new page, description copied from its frontmatter.
7. Add an entry to `log.md`, at the top.
   Run `tools/okf-lint.py` before reporting.
8. **Report after.** The takeaways, the judgment calls made — what got split,
   merged, or deliberately left out — and anything thin, unverified, or worth a
   second source. This is where emphasis gets steered; revise in place from there.

Uncertainty is not a reason to pause. File the page with the doubt marked on it —
`> [!warning] Unsourced`, a thin-page callout, an *(inferred)* tag — and say so in
the report. A flagged page beats a question that stalls the ingest.

## Query

Trigger: the human asks a question.

1. Read `index.md` first, then drill into the relevant pages. Read `raw/` only
   when the wiki is insufficient — if that happens often, the wiki has a gap
   worth fixing.
2. Answer with citations as `[[wikilinks]]`.
3. **Offer to file good answers back into the wiki** as a `synthesis` page.
   An analysis that dies in chat history is wasted work. This is how exploration
   compounds, not just ingestion.
4. If the answer required a synthesis page, update `index.md` and `log.md` too.

## Research

Trigger: "what do we have on X", "find material for [[Piece]]".

1. Search `wiki/` first, then `raw/`. Web search only when the vault comes up dry —
   and say plainly which claims came from outside it.
2. Report in chat with `[[wikilinks]]`, and file the material under the piece's
   workbench heading if it has one.
3. **Durable findings belong in the wiki, not the workbench.** If it would be
   true regardless of this essay, it is a `concept` or `synthesis` page — write
   it there and link to it from below the line. Research that lives only inside
   one draft dies with that draft.

## Edit

Trigger: "edit this", "line-edit X", "does this argument hold".

1. Read `writing/STYLE.md`, then the piece in full.
2. **Default to critique, not surgery.** Report on argument, structure, evidence,
   and where a claim outruns its support. Touch the prose only when asked for a
   line edit outright.
3. Move cut material below the line rather than deleting it.
4. Update `generated.at` in frontmatter — `generated.by` stays `human:bonan`. Add
   to `log.md`.

## Publish

Trigger: "this is published", or "shipped X".

1. Set `status: published`, fill in `url` and `venue`, update `generated.at`.
2. **Harvest.** Every argument the piece makes that the wiki does not yet hold
   becomes a `synthesis` page, citing the essay as its origin. This is the loop
   that makes the next piece cheaper to write — do not skip it.
3. Offer to clear the workbench.
4. Update `index.md`. Add an entry to `log.md`, at the top.

## Lint

Trigger: "lint the wiki", or roughly every 10 ingests.

Start with `tools/okf-lint.py`, which covers everything mechanical. Then report,
do not auto-fix — bring findings to the human first:

- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages (no inbound links)
- Concepts referenced repeatedly but lacking a page
- Missing cross-references (page A discusses B without linking it)
- Broken wikilinks
- Frontmatter drift (missing `generated`, wrong `type`, index description out of
  sync with the page) — `okf-lint.py` finds these
- Pages stuck at `status: draft`, and what they are missing
- Pages worth proposing for `verified` — well-sourced, unlikely to change, and
  cheap for the human to confirm in one read
- Data gaps a web search or new source could fill
- Published pieces never harvested into the wiki
- Drafts stalled a long time, and what they are missing
- **Open questions worth investigating** — the most valuable output. Suggest what
  to read next.

# Logging

`log.md` follows OKF §9: date-grouped, **newest first**, ISO 8601 headings. A new
entry goes at the top of the file, under today's date heading, creating that
heading if it does not exist yet:

```markdown
## 2026-08-11

* **Ingest**: Article Title.

  What changed, which pages were touched. 1-3 short paragraphs, indented under
  the bullet.
```

Op is the bold label — one of `Ingest`, `Query`, `Research`, `Edit`, `Publish`,
`Lint`, `Refactor` — which keeps the log greppable:
`grep '^\* \*\*' log.md | head -5`.

**Append-only is a discipline, not a file position.** Entries are added, never
rewritten, reordered, or deleted, even though new ones now go on top. Correcting a
past entry means writing a new one that says what changed.

# Hard rules

1. **Never modify anything in `raw/`.** It is the source of truth. Read only.
   Derived text belongs in `extracted/`, which is agent-owned, regenerable, and
   never hand-edited by either of us.
2. **Never write prose above the line in `writing/`.** Not a first draft, not a
   transition sentence, not a filled-in `TODO`. Editing on request is fine;
   originating is not. If a piece needs a paragraph, say what it needs and let
   the human write it.
3. **Never delete a wiki page** without asking. Merging is usually the right move.
4. **Every ingest touches `index.md` and `log.md`.** No exceptions — a wiki whose
   index has drifted from its contents is worse than no index.
5. **Do not invent facts.** The wiki's value is that it is traceable. If something
   is inference rather than source, say so inline: *(inferred)*. This extends to
   frontmatter: never write a `verified` entry the human did not give you, and
   never fill a date field with a fabricated precision.
6. Use relative paths from vault root. No leading slash.
7. **Keep the bundle conformant.** `tools/okf-lint.py` must pass before you report
   an operation finished. A new deviation from OKF gets written into the table
   under [Format](#format) — never taken silently.

# Tools

- `tools/wiki-search.sh <query>` — ripgrep `wiki/` with context. `-w` adds
  `writing/`, `-s` searches sources (`raw/` + `extracted/`), `-a` searches
  everything, `-t` matches titles only.
- `tools/extract.sh` — render every non-text source in `raw/` to searchable plain
  text in `extracted/`. Idempotent, so it is safe to run any time; `-f` forces a
  rebuild. Unknown formats and missing tools are reported, never silently
  skipped. Format coverage: `extracted/README.md`.
- `tools/okf-lint.py` — check the vault against [[Open Knowledge Format]] v0.2 and
  against this schema: frontmatter parses, `type` is non-empty and known, actors
  follow the convention, `sources[].resource` paths exist, `status` is in
  vocabulary, and every wiki page appears in `index.md` with a matching
  description. Reports only, never fixes. No dependencies beyond python3. `-q`
  prints errors only.
- Scale-up path if the index stops being enough: [qmd](https://github.com/tobi/qmd),
  a local hybrid BM25/vector search over markdown, with CLI + MCP.

# Evolving this file

This schema is a living document — co-evolve it with the human. When a convention
proves awkward, or a new page type or workflow earns its place, propose the edit
to this file explicitly rather than quietly diverging from it.
