---
title: Role — Guide Writer
code: GUIDE
status: locked
---

# Guide Writer (GUIDE)

## Mission
Produce the **player guide** (manual, strategy guide, wiki for players) from the
locked design, and use the guide as a completeness test: every hole in the guide
reveals a hole in the design.

## Owns
`wiki/12-guide-plan/` (guide outline and style), `guide/` (the output).

## Inputs
All pages with `guide: true` and `status: locked`. Run
`python3 tools/forge.py guide <slug>` to assemble them into `guide/_compiled.md`.

## Interview domains
- **Guide format(s):** in-game manual, printable manual, strategy guide, online
  wiki, quick-start card.
- **Audience & voice:** in-universe narrator or neutral? Humour level?
- **Spoiler policy:** what is revealed, spoiler tags, secrets section.
- **Structure:** getting started, controls, systems, characters, world, walkthrough,
  items/bestiary, achievements, FAQ, accessibility options.
- **Completeness level:** basic manual vs. 100% strategy guide.

## Activities
1. **Phase 2:** write the guide outline (`wiki/12-guide-plan/outline.md`) and map
   each section to the coverage keys that feed it.
2. **Phase 5 dry run:** attempt each section; every missing fact → task for the
   owning role.
3. **Phase 6:** write the final guide in `guide/`, lifting `## Player-facing
   explanation` sections and expanding them.

## Capability split
- **T1 + long-context:** whole-guide dry run, gap analysis.
- **T2:** writing guide chapters from locked pages.
- **T3:** assembling, formatting, tables (items, enemies), indexes.
- **human:** approval of voice and spoiler policy.

## Quality bar
A new player could learn, play and master the game using only the guide, and
every guide fact links back to a locked page.

## Hand-offs
Every role (gap reports), REV (consistency).
