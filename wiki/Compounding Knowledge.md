---
type: concept
title: "Compounding Knowledge"
description: "Why a maintained wiki gets cheaper to query as it grows, unlike retrieval."
created: 2026-08-11
generated: { by: claude-code/claude-opus-5, at: 2026-08-11 }
status: stable
sources:
  - id: karpathy-llm-wiki
    resource: "raw/llm-wiki-karpathy.md"
    title: "LLM Wiki"
    author: human:andrej-karpathy
    published: 2026
tags: [knowledge-management, rag, llm]
---

# Compounding Knowledge

The property that distinguishes a maintained wiki from a retrieval index: synthesis
is written down once and then kept current, so each new source makes every future
question cheaper to answer rather than more expensive ([[LLM Wiki (Karpathy)]]).

## The contrast

| | Retrieval (RAG) | Maintained wiki |
|---|---|---|
| When synthesis happens | At query time, every time | At ingest time, once |
| Cross-references | Rediscovered per query | Already written |
| Contradictions | Surface silently, if at all | Flagged when the conflict lands |
| Effect of a new source | One more chunk in the pile | Revises the existing picture |
| Artifact left behind | None — answers die in chat | A persistent, growing wiki |

## Why it compounds

Three mechanisms, all of which fail in a pure retrieval setup:

1. **Integration on arrival.** A source is not merely indexed — it is read against
   what is already known, and existing pages are revised to reflect it. The
   comparison work is done while the source is in context.
2. **Explicit contradiction handling.** New data that disputes an old claim gets
   marked at ingest, when both sides are visible. A retrieval system just returns
   both chunks and hopes.
3. **Queries feed back.** A good answer becomes a `synthesis` page rather than
   evaporating, so exploration accumulates alongside ingestion. This is the step
   most easily skipped and the one that does the most compounding.

## The cost that makes it possible

The pattern is not new — the bottleneck was always maintenance. Cross-references
rot, summaries go stale, consistency across dozens of pages decays, and the burden
grows faster than the value, so humans abandon their wikis. What changed is that an
LLM can touch fifteen files in one pass and does not get bored, driving the marginal
cost of maintenance toward zero ([[LLM Wiki (Karpathy)]]). The same observation
retroactively explains the [[Memex]]'s missing piece.

## Consequence for this vault

If the agent routinely has to read `raw/` to answer a question, the wiki is not
compounding — that is a gap to fix, not a workflow. See the Query operation in
[[CLAUDE.md]].

---
*Related: [[LLM Wiki (Karpathy)]], [[Memex]]*
