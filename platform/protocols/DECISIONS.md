---
title: Decision Protocol
status: locked
---

# Decision Protocol

A **decision record** is the atomic unit of truth. Wiki pages are explanations
built on decisions; if a page and a decision disagree, the decision wins.

## Where decisions live
`projects/<slug>/decisions/D-<ROLECODE>-<NNNN>.md`
ID: `python3 tools/forge.py id <slug> decision <ROLECODE>`.

## Frontmatter

```yaml
---
id: D-SYS-0007
title: Health recovers only via consumables
role: systems-designer
status: locked            # proposed | locked | superseded
source: owner             # owner | delegated
question: Q-SYS-0002#Q3   # where the answer came from
supersedes:               # D-* this replaces (if any)
superseded_by:            # filled in later if replaced
affects: [wiki/01-mechanics/health.md, wiki/08-economy/consumables.md]
date: 2026-11-03
---
```

## Body

```markdown
## Decision
Player health recovers only by using consumable items. No passive regeneration.

## Rationale
Supports pillar P2 "every resource is a choice" (D-CD-0003).

## Consequences
- 08-economy must define consumable sources and costs (T-ECO-0004 created).
- 03-levels must place recovery items (T-LVL-0009 created).

## Creative Owner's words (verbatim)
> "B, definitely. I want people hoarding potions."
```

## Rules
1. **Absolute language** in `## Decision`: one to three sentences, no hedging.
2. A decision is `locked` only if `source` is `owner` or `delegated` **and**
   `question` points to a real answered question. Agents may create `proposed`
   decisions to bundle into a confirmation question.
3. **Consequences create tasks.** If a decision affects another discipline,
   create a task for that role in the same session.
4. **Changing a locked decision**: never edit the decision text. Create a new
   decision with `supersedes: <old ID>`, set the old one to `status: superseded`
   and `superseded_by: <new ID>`, then open tasks to update every file in `affects`.
   Changes to a locked decision always require a fresh owner answer.
5. **Pages cite decisions** in their frontmatter `decisions:` list and inline as
   `(D-SYS-0007)`.
6. **Conflicts** between two locked decisions → the Reviewer raises a `blocking`
   question to the Creative Owner presenting both. Never silently pick one.
