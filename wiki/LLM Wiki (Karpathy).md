---
type: source
created: 2026-08-11
updated: 2026-08-11
sources: 1
source: "[[raw/llm-wiki-karpathy.md]]"
author: Andrej Karpathy
source_date: 2026
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
tags: [knowledge-management, llm, wiki]
---

# LLM Wiki (Karpathy)

An idea file describing a pattern in which an LLM agent incrementally builds and
maintains a personal wiki over a curated set of raw sources, instead of retrieving
from those sources fresh on every query. It is the source document for this vault's
own design ([[CLAUDE.md]]).

## Core claim

Standard RAG rediscovers knowledge on every question — nothing accumulates. A
question requiring synthesis across five documents forces the model to find and
reassemble the same fragments every time. The alternative is to compile knowledge
*once* into a structured, interlinked artifact and then keep it current. See
[[Compounding Knowledge]].

The human's role is sourcing, exploration, and asking good questions. The LLM's
role is everything else: summarizing, cross-referencing, filing, bookkeeping.
Karpathy's own setup runs the agent on one side and Obsidian on the other, browsing
edits live — *"Obsidian is the IDE; the LLM is the programmer; the wiki is the
codebase."*

## Three-layer architecture

1. **Raw sources** — immutable, curated, never modified by the LLM.
2. **The wiki** — LLM-generated markdown; the LLM owns this layer entirely.
3. **The schema** — a `CLAUDE.md` / `AGENTS.md` that encodes conventions and
   workflows. Karpathy calls this the key configuration file: it is what makes the
   model a disciplined maintainer rather than a generic chatbot. It is meant to be
   co-evolved by human and LLM over time.

## Three operations

- **Ingest** — read a new source, discuss takeaways, write a summary page, update
  affected pages across the wiki (*"a single source might touch 10-15 wiki pages"*),
  update the index, append to the log.
- **Query** — read the index, drill into pages, answer with citations. The load-bearing
  insight: good answers should be **filed back into the wiki** as new pages, so
  exploration compounds the same way ingestion does.
- **Lint** — periodic health check for contradictions, stale claims, orphan pages,
  missing cross-references, and gaps worth researching.

## Navigation files

`index.md` is content-oriented (a catalog by category, read first on every query);
`log.md` is chronological and append-only. Karpathy notes a consistent entry prefix
makes the log greppable with plain unix tools. He claims the index approach works
without embedding-based retrieval up to roughly 100 sources / hundreds of pages —
beyond that, a real search tool like [qmd](https://github.com/tobi/qmd) earns its keep.

## Why it works

The failure mode of human wikis is not reading or thinking — it is bookkeeping.
Maintenance burden grows faster than value, so wikis get abandoned. LLMs do not get
bored and can touch fifteen files in one pass, so maintenance cost approaches zero.
Karpathy links the idea to Vannevar Bush's [[Memex]], whose unsolved problem was
precisely who does the maintenance.

## Scope note

The gist is deliberately abstract — it specifies the pattern, not an implementation.
Directory structure, page formats, and tooling are explicitly left to be instantiated
per domain. This vault's instantiation lives in [[CLAUDE.md]].

## Applicable contexts

Personal tracking (goals, health, psychology), long-running research, reading a book
with a companion wiki, team/business wikis fed by transcripts and threads, plus
competitive analysis, due diligence, trip planning, and course notes.

---
*Source: [[raw/llm-wiki-karpathy.md]] · Related: [[Compounding Knowledge]], [[Andrej Karpathy]], [[Memex]]*
