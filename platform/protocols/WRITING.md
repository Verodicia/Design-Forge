---
title: Writing Protocol
status: locked
---

# Writing Protocol — How Wiki Pages Are Written

## Page frontmatter (required on every wiki page)

```yaml
---
title: Health & Damage
owner: systems-designer       # role that owns this page
status: draft                 # stub | exploring | draft | locked | n/a | superseded
guide: true                   # contains player-facing facts for the guide
decisions: [D-SYS-0007, D-SYS-0008]
coverage: 01-mechanics/health # coverage key this page answers
updated: 2026-11-03
---
```

## Page structure
Use these headings in this order, omitting ones that don't apply:

1. `# Title`
2. `## Summary`: 1–3 absolute sentences. Someone reading only this knows the rule.
3. `## Specification`: the full rules, precisely. Prefer tables and numbered lists.
4. `## Values`: every number in a table: name, value, unit, tunable range, owner.
5. `## Edge cases`: what happens at limits, on failure, when interrupted, offline, etc.
6. `## Player-facing explanation`: plain-language text the Guide Writer can lift
   directly (required when `guide: true`).
7. `## Dependencies`: links to pages this relies on / affects.
8. `## Open questions`: **only allowed when status is not `locked`.** Each item
   links to a `Q-*` batch.

Template: [templates/page.md](../templates/page.md).

## Absolute language
In `locked` pages these words are **banned** (the validator flags them):
`maybe, might, perhaps, possibly, probably, could be, TBD, TODO, to be decided,
we'll see, something like, roughly, ideally, hopefully, ???`

Write: *"Enemies drop 1–3 coins (uniform random)."*
Not: *"Enemies should probably drop a few coins."*

Ranges are absolute if they are exact ("1–3", "tunable 0.8–1.2 by Balancing").

## Conventions
- **Links** are relative markdown links. Cite decisions inline: `(D-SYS-0007)`.
- **Glossary:** every game-specific term is defined once in `wiki/glossary.md`
  (owned by the Reviewer). Bold the term on first use in a page and link it.
- **Units:** SI and seconds; currency names as defined by Economy.
- **Names:** lowercase-kebab-case file names. One topic per page. Split pages
  over ~400 lines.
- **Lists of content** (enemies, items, levels) are tables with a stable `id` column.
- **No duplication:** if you need a fact owned by another page, link it; don't restate it.
- **Diagrams:** Mermaid inside markdown (flowchart, stateDiagram, sequenceDiagram).
- **Images:** store in `wiki/<discipline>/assets/`, reference relatively, and add a
  caption stating whether it is *reference*, *concept*, or *approved*.

## Coverage map rows
Each discipline `index.md` has a `## Coverage map` table:

```markdown
| key | topic | tier | needs | phase | status | page | ref |
|---|---|---|---|---|---|---|---|
| `core-loop` | Core loop at moment / minute / session scale | T1 | | 3 | locked | [core-loop](core-loop.md) | D-SYS-0002 |
```
- `key`: stable, kebab-case, backticked. Never rename.
- `tier` / `needs` / `phase`: defaults used when `forge.py decompose` creates the task.
- `status`: same vocabulary as pages (`stub`, `exploring`, `draft`, `locked`, `n/a`).
- `ref`: the active task (`T-*`) while open; the deciding decision(s) (`D-*`) once locked.

When you finish a page, update its row in the same edit session. To add a topic
the game needs, append a row with `status: stub` and an empty `ref`.
