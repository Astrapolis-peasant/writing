---
type: source
title: "Open Knowledge Format"
description: "Google's v0.2 spec for agent-maintained knowledge bundles: markdown plus frontmatter, with provenance, trust, and lifecycle made first-class."
resource: "raw/okf-spec-v0.2.md"
created: 2026-08-17
generated: { by: claude-code/claude-opus-5, at: 2026-08-17 }
status: stable
sources:
  - id: okf-spec-v0.2
    resource: "raw/okf-spec-v0.2.md"
    title: "Open Knowledge Format (OKF) v0.2 specification"
    author: team:gcp-knowledge-catalog
    published: 2026
url: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
tags: [knowledge-management, format, provenance, interoperability]
---

# Open Knowledge Format

A minimal specification for knowledge corpora that agents write and maintain: a
directory of markdown files with YAML frontmatter, no schema registry, no central
authority, no required tooling. This vault conforms to v0.2 — the schema in
[[CLAUDE.md]] documents where and how.

## The problem it names

The spec's premise is that a knowledge corpus is no longer authored once and then
read; it is *continuously written by agents*. That shift makes five questions
first-class that plain markdown leaves implicit: provenance (what was this made
from), trust (how much should I believe it), freshness (is it still true),
lifecycle (is it current), and attestation (was this number produced the sanctioned
way). Everything OKF standardizes exists to answer one of those five.

It is the same diagnosis [[LLM Wiki (Karpathy)]] makes from the other end.
Karpathy's gist specifies the *workflow* an agent-maintained wiki needs and leaves
the file format to the implementer; OKF specifies the *format* and leaves the
workflow alone. They compose almost without friction, which is why this vault can
run both.

## What it standardizes

A **bundle** is a directory tree. `index.md` and `log.md` are reserved at any
level — directory listing and change history. Every other `.md` file is a
**concept**, and the only always-required frontmatter key is `type`, which is
deliberately unregistered: producers invent type names, consumers must tolerate
unknown ones.

Three optional frontmatter families carry the weight:

- **`sources`** — a list of what the concept derives from, each with a required
  `resource` and optional credibility signals (`author`, `usage_count`,
  `last_modified`). Per-claim attribution uses markdown footnotes keyed to a
  source's `id` rather than a position in the list, on the reasoning that agents
  constantly rewrite these documents and a positional index misattributes silently
  the moment the list is reordered.
- **`generated` and `verified`** — who produced the content and who has since
  confirmed it, kept separate because the writer need not be the checker. Both use
  one actor convention: `<producer>/<version>` for agents, `human:<id>` for people,
  `process:<id>` for automation.
- **`status` and `stale_after`** — `draft | stable | deprecated`, plus an absolute
  expiry date rather than a relative TTL, so staleness is a plain date comparison.

## The design move worth stealing

OKF records **signals, not verdicts**. It stores `usage_count` and `last_modified`
but no credibility score; it stores verification events but no trust level. Trust
tiers — unverified, machine-confirmed, human-reviewed — are *derived* by the
consumer from whether a `human:` actor appears in `verified`. The stated reason is
that a score is subjective, unportable across consumers, and goes stale, whereas
the signals it was computed from do not. The same instinct runs through this vault's
insistence on attribution over assertion ([[Compounding Knowledge]]).

## Attested Computation

The ambitious part, and the part this vault has no use for. A concept of
`type: Attested Computation` carries a sanctioned computation, typed parameters an
agent may fill but never edit, an executor that returns a receipt, and a
deterministic no-LLM attester that checks the receipt against the sanctioned
computation. The point is to make "did the blessed query actually run" a mechanical
comparison rather than a judgement call. OKF distinguishes this from `verified`:
verification confirms a *definition* still matches policy and is stored in the
bundle; attestation confirms a single *run* and is not stored at all.

## Conformance is deliberately weak

Three rules only: parseable frontmatter on every non-reserved file, a non-empty
`type` in each, and reserved filenames following their prescribed shape. Consumers
are forbidden from rejecting a bundle for unknown types, unknown keys, missing
optional fields, broken cross-links, or a missing `index.md`. Broken links are
explicitly *not* malformed — they may be knowledge not yet written, which is a
generous reading this vault already relies on.

---
*Source: [[raw/okf-spec-v0.2.md]] · Related: [[LLM Wiki (Karpathy)]], [[Compounding Knowledge]], [[CLAUDE.md]]*
