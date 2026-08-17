---
type: readme
title: "Extracted text"
description: "Plain-text renderings of every non-text source in raw/, so binaries are searchable."
created: 2026-08-12
generated: { by: claude-code/claude-opus-5, at: 2026-08-12 }
status: stable
tags: [meta, tooling]
---

# Extracted text

Plain-text renderings of every non-text source in `raw/`, so they can be searched.
A PDF is opaque to ripgrep; `Book.pdf.txt` is not.

**Agent-owned and derived — never edit by hand.** Fix the source or the extractor,
then re-run. Anything typed here is lost on the next `-f` pass.

## How it works

```
tools/extract.sh          extract sources that are new or changed
tools/extract.sh -f       re-extract everything
tools/extract.sh FILE...  extract specific files
```

Naming keeps the original extension so the mapping back is unambiguous and two
sources with the same stem cannot collide:

```
raw/Esther-Vilar-The-Manipulated-Man.pdf  →  extracted/Esther-Vilar-The-Manipulated-Man.pdf.txt
```

Files already plain text (`.md`, `.txt`, `.csv`, `.json`, `.yaml`) are skipped —
ripgrep reads those out of `raw/` directly.

## Coverage

| Format | Tool | Status |
|---|---|---|
| `.pdf` | `pdftotext` (poppler) | installed |
| `.doc .docx .odt .rtf .html .webarchive` | `textutil` | built into macOS |
| `.epub .tex .rst .org` | `pandoc` | install if needed |
| `.png .jpg .tiff` | `tesseract` | install if needed |

Unknown formats are reported and skipped, never silently dropped. Missing tools
print the exact `brew install` line.

## Why it is committed

This is what the agent actually read. The wiki cites claims traceable to these
files, not to the binary originals, so keeping them in git means provenance
survives on any clone — and search works without the extraction toolchain
installed. Text compresses well; if it ever bloats the repo, add `extracted/` to
`.gitignore` and regenerate on demand instead.

## Searching

`tools/wiki-search.sh -a "query"` covers this directory. Scans have OCR noise —
expect the odd `clue` for `due` — so prefer short distinctive phrases over exact
long strings.
