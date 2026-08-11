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
