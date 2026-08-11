# Wiki Schema

This vault is an **LLM wiki** ([Karpathy's pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)).
Not a RAG index — a persistent, compounding artifact that you maintain and I read.

**Division of labor:** the human curates sources, directs analysis, and asks
questions. The agent writes and maintains *everything* under `wiki/`, plus
`index.md` and `log.md`. The human should rarely need to edit a wiki page by hand;
if they do, that is a signal the schema needs updating.

## Layout

```
raw/            immutable sources — READ ONLY, never edit or delete
raw/assets/     images and attachments for sources
wiki/           agent-owned markdown pages (flat, wikilinked)
index.md        catalog of every wiki page, by category
log.md          append-only chronological record
tools/          helper scripts
CLAUDE.md       this file — the schema
```

`wiki/` is deliberately **flat**. Obsidian resolves `[[Page Name]]` by filename, so
folders buy nothing and cost churn. Categorization lives in `index.md` and in each
page's `type` frontmatter field.

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

## Operations

### Ingest

Trigger: a new file lands in `raw/`, or the human says "ingest X".

1. Read the source in full. If it embeds images, read the text first, then view
   the images in `raw/assets/` separately for extra context.
2. **Discuss takeaways with the human before writing.** Do not silently file a
   source — the conversation is where the human steers emphasis. Skip this only
   if explicitly told to batch-ingest.
3. Write a `source` page in `wiki/` summarizing it.
4. Propagate: update every existing entity/concept/synthesis page the source
   touches. A single good source often moves 10-15 pages. Do not stop at one.
5. Create new entity/concept pages for anything substantial that lacks a page.
6. Update `index.md`.
7. Append to `log.md`.

### Query

Trigger: the human asks a question.

1. Read `index.md` first, then drill into the relevant pages. Read `raw/` only
   when the wiki is insufficient — if that happens often, the wiki has a gap
   worth fixing.
2. Answer with citations as `[[wikilinks]]`.
3. **Offer to file good answers back into the wiki** as a `synthesis` page.
   An analysis that dies in chat history is wasted work. This is how exploration
   compounds, not just ingestion.
4. If the answer required a synthesis page, update `index.md` and `log.md` too.

### Lint

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
- **Open questions worth investigating** — the most valuable output. Suggest what
  to read next.

## Logging

`log.md` is append-only, newest at the bottom. Every entry starts with a fixed
prefix so it stays greppable:

```
## [2026-08-11] ingest | Article Title
```

Op is one of `ingest`, `query`, `lint`, `refactor`. Follow the heading with 1-3
lines: what changed, which pages were touched. `grep "^## \[" log.md | tail -5`
should give a useful recent history.

## Hard rules

1. **Never modify anything in `raw/`.** It is the source of truth. Read only.
2. **Never delete a wiki page** without asking. Merging is usually the right move.
3. **Every ingest touches `index.md` and `log.md`.** No exceptions — a wiki whose
   index has drifted from its contents is worse than no index.
4. **Do not invent facts.** The wiki's value is that it is traceable. If something
   is inference rather than source, say so inline: *(inferred)*.
5. Use relative paths from vault root. No leading slash.

## Tools

- `tools/wiki-search.sh <query>` — ripgrep across `wiki/` and `raw/` with context.
- Scale-up path if the index stops being enough: [qmd](https://github.com/tobi/qmd),
  a local hybrid BM25/vector search over markdown, with CLI + MCP.

## Evolving this file

This schema is a living document — co-evolve it with the human. When a convention
proves awkward, or a new page type or workflow earns its place, propose the edit
to this file explicitly rather than quietly diverging from it.
