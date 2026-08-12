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
index.md        catalog of every wiki page and piece, by category
log.md          append-only chronological record
tools/          helper scripts
CLAUDE.md       this file — the schema
```

Both `wiki/` and `writing/` are deliberately **flat**. Obsidian resolves
`[[Page Name]]` by filename, so folders buy nothing and cost churn.
Categorization lives in `index.md` and in each page's `type` frontmatter field.

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
type: source            # source | entity | concept | synthesis
created: 2026-08-11
updated: 2026-08-11
sources: 1              # how many raw sources feed this page
tags: [knowledge-management]
---
```

`source` pages add `source: "[[raw/file.md]]"`, `author:`, and `source_date:`.

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
| Edit frontmatter (`status`, `updated`, `url`, `venue`) | |

When asked for a line edit: prefer a cut to a rewrite, and never replace a
sentence that already works. Read `writing/STYLE.md` first, every time.

### Frontmatter

```yaml
---
type: essay
status: draft           # seed | draft | published | shelved
created: 2026-08-11
updated: 2026-08-11
venue:                  # where it is going, or where it went
url:                    # filled in on publish
tags: [knowledge-management]
---
```

`type` is `essay` for everything with an audience — posts, essays, threads.

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
6. Update `index.md`.
7. Append to `log.md`.
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
4. Update `updated` in frontmatter. Append to `log.md`.

## Publish

Trigger: "this is published", or "shipped X".

1. Set `status: published`, fill in `url` and `venue`, update `updated`.
2. **Harvest.** Every argument the piece makes that the wiki does not yet hold
   becomes a `synthesis` page, citing the essay as its origin. This is the loop
   that makes the next piece cheaper to write — do not skip it.
3. Offer to clear the workbench.
4. Update `index.md`. Append to `log.md`.

## Lint

Trigger: "lint the wiki", or roughly every 10 ingests.

Report, do not auto-fix — bring findings to the human first:

- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages (no inbound links)
- Concepts referenced repeatedly but lacking a page
- Missing cross-references (page A discusses B without linking it)
- Broken wikilinks
- Frontmatter drift (missing `updated`, wrong `type`)
- Data gaps a web search or new source could fill
- Published pieces never harvested into the wiki
- Drafts stalled a long time, and what they are missing
- **Open questions worth investigating** — the most valuable output. Suggest what
  to read next.

# Logging

`log.md` is append-only, newest at the bottom. Every entry starts with a fixed
prefix so it stays greppable:

```
## [2026-08-11] ingest | Article Title
```

Op is one of `ingest`, `query`, `research`, `edit`, `publish`, `lint`,
`refactor`. Follow the heading with 1-3 lines: what changed, which pages were
touched. `grep "^## \[" log.md | tail -5` should give a useful recent history.

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
   is inference rather than source, say so inline: *(inferred)*.
6. Use relative paths from vault root. No leading slash.

# Tools

- `tools/wiki-search.sh <query>` — ripgrep `wiki/` with context. `-w` adds
  `writing/`, `-s` searches sources (`raw/` + `extracted/`), `-a` searches
  everything, `-t` matches titles only.
- `tools/extract.sh` — render every non-text source in `raw/` to searchable plain
  text in `extracted/`. Idempotent, so it is safe to run any time; `-f` forces a
  rebuild. Unknown formats and missing tools are reported, never silently
  skipped. Format coverage: `extracted/README.md`.
- Scale-up path if the index stops being enough: [qmd](https://github.com/tobi/qmd),
  a local hybrid BM25/vector search over markdown, with CLI + MCP.

# Evolving this file

This schema is a living document — co-evolve it with the human. When a convention
proves awkward, or a new page type or workflow earns its place, propose the edit
to this file explicitly rather than quietly diverging from it.
