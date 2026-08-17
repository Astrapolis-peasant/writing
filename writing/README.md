---
type: readme
title: "Writing"
description: "How the human-owned half of the vault works — the line, the status ladder, and what to ask the agent for."
created: 2026-08-11
generated: { by: claude-code/claude-opus-5, at: 2026-08-17 }
status: stable
tags: [meta, writing]
---

# Writing

Essays and posts headed for an audience. One file per piece, flat — the title is
the filename, in natural language.

**You write these.** The agent researches, critiques, and line-edits on request,
but it does not originate prose here. Full rules in `CLAUDE.md`.

## The line

Every piece is split by a `---` horizontal rule. Above it is the essay; below it
is the workbench.

```markdown
---
type: essay
title: "The title, again"
description: "One sentence — what the piece argues."
status: draft
created: 2026-08-11
generated: { by: human:bonan, at: 2026-08-11 }
venue:
url:
tags: []
---

The essay. Every sentence here is yours.

---

## Notes

Below the line the agent writes freely — research, citations, cut paragraphs.
Create the headings you want it to use. Stripped at publish time.
```

Create a `## Notes`, `## Sources`, or `## Cuts` heading and the agent will file
material under it. No heading, no workbench — it stays in chat.

## Status ladder

`seed` → `draft` → `published`, plus `shelved` for anything set down.

A `seed` can be three lines. Don't let the ladder become a reason not to open a
file.

## Working with the agent

| Say | You get |
|---|---|
| "what do we have on X" | A brief from the wiki, with `[[wikilinks]]`, filed to the workbench |
| "does this argument hold" | Critique only — nothing in the file changes |
| "line-edit this" | Cuts and tightening, voice preserved, cut material moved below the line |
| "this is published" | Frontmatter updated, then the arguments harvested into wiki pages |

That last one is the point of the whole setup: a finished essay pays back into
the wiki, so the next one starts further along.

## Voice

`STYLE.md` is what the agent reads before touching a word. It starts empty —
fill it in as you notice your own rules, and it gets more useful the more
specific it is.
