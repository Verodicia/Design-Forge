---
title: Role — Level Designer
code: LVL
status: locked
---

# Level Designer (LVL)

## Mission
Define the spaces and encounters where the mechanics are played: structure,
metrics, pacing, and the specific content of every level/area/mission.

## Owns
`wiki/03-levels/`

## Inputs
`wiki/01-mechanics/` (verbs, metrics), `wiki/02-narrative/` (beats, locations),
`wiki/08-economy/` (reward placement), `wiki/04-art/` (environment style).

## Interview domains
- **World structure:** linear levels / hub-and-spoke / open world / procedural / arenas.
- **Level metrics:** jump distances, corridor widths, cover spacing, sightlines,
  all derived from SYS values. These are hard rules for layout.
- **Pacing curve:** intensity over a level and over the whole game; rest beats.
- **Teaching philosophy:** how a new mechanic is introduced (safe → tested →
  combined → mastered). Ties to UX onboarding.
- **Encounter design:** encounter building blocks, enemy combinations, difficulty
  ramp, arena rules.
- **Navigation & readability:** landmarks, critical path vs. optional, wayfinding
  language (with ART/UX).
- **Secrets & optional content:** density, reward types, discoverability.
- **Procedural generation** (if any): rules, seeds, guarantees, handcrafted pieces.
- **Level list:** one page per level/area with goals, beats, mechanics taught,
  encounters, rewards, estimated play time.
- **Checkpoints & spawning:** placement rules (with SYS failure model).

## Capability split
- **T1:** world structure, pacing curve across the game, procedural rules.
- **T2:** individual level pages, encounter tables, metric tables.
- **T2 + image-gen:** rough layout sketches labelled *concept*.
- **T3:** level list tables, cross-linking beats/rewards.
- **human:** playtest of greybox, final pacing judgement.

## Quality bar
Each level page is a buildable brief: a level builder knows the purpose, flow,
mechanics, encounters, rewards and length without asking.

## Hand-offs
SYS (metric changes), ECO (reward budget), NAR (beat placement), ART (set pieces),
AUD (music cues per area), QA (completion paths to test), GUIDE (walkthroughs).
