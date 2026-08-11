# Raw sources

Immutable source documents. **The agent reads these and never edits them.**

Drop things here, then tell the agent to ingest. Anything that survives as
markdown works: clipped articles, papers, transcripts, notes, exports.

- Images and attachments go in `raw/assets/`.
- Keep original filenames where they are informative; otherwise use a short
  descriptive slug (`llm-wiki-karpathy.md`).
- Optional frontmatter helps ingestion — `title`, `author`, `source_date`, `url`.

**Getting sources in:** [Obsidian Web Clipper](https://obsidian.md/clipper)
converts web articles to markdown. To pull images local, bind
*Download attachments for current file* to a hotkey (Settings → Hotkeys) —
the attachment folder is already set to `raw/assets/`.
