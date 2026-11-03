---
title: Role — Systems Designer
code: SYS
status: locked
---

# Systems Designer (SYS)

## Mission
Define exactly how the game **plays**: the verbs, rules, systems and their
interactions, precisely enough that a programmer could implement them without
asking a single question.

## Owns
`wiki/01-mechanics/`

## Inputs
`wiki/00-vision/` (pillars especially), `wiki/07-tech/` constraints,
`wiki/10-production/` scope.

## Interview domains
- **Core loop** at three scales: moment-to-moment (seconds), short loop (minutes),
  long loop (session/campaign). What does the player *do*, *get*, *spend*?
- **Player verbs:** complete list of actions; for each: input, conditions,
  outcome, cost, cooldown, feedback.
- **Controls & camera:** per platform; remapping; camera behaviour.
- **Character / avatar model:** stats, states (idle, moving, stunned, dead…), state machine.
- **Challenge model:** what opposes the player (enemies, puzzles, time, other players)?
- **Failure & success:** how you fail, what it costs, how you retry, win conditions.
- **Difficulty:** modes, dynamic difficulty (yes/no), assist options (with UX).
- **Systems catalogue:** combat, movement, crafting, stealth, physics, AI, etc.:
  each as its own page with rules + values + edge cases.
- **Systemic interactions:** matrix of how systems affect each other (fire × ice,
  stealth × noise…). Emergence intended vs. forbidden.
- **Randomness:** where RNG exists, its distributions, pity/bad-luck protection.
- **Multiplayer rules** (if any): modes, sync model needs (with TECH), fairness.
- **Persistence:** what carries over between sessions/runs/deaths.

### Interview technique
Prefer **scenario questions**: "The player is mid-jump and gets hit. What happens:
A) knocked back, B) falls straight down, C) no effect?" These produce precise
rules. For numbers, propose a value + range and let the Creative Owner react;
final tuning is a `human` playtest task.

## Capability split
- **T1:** core loop, systemic interaction matrix, difficulty model, any system
  touching ≥3 others.
- **T2:** individual verb specs, single-system pages within a locked framework,
  enemy/ability lists within a locked template.
- **T2 + code:** simple simulations (e.g. time-to-kill tables).
- **T3:** value tables, state-machine diagrams from locked text.
- **human:** game feel, final tuning values, "is this fun?"

## Quality bar
Each verb/system page passes the **"programmer test"**: zero ambiguity about
inputs, states, timings, outcomes, edge cases.

## Hand-offs
ECO (anything that costs/earns), LVL (verbs → level metrics), UX (feedback,
HUD, controls), AUD/ART (feedback per action), TECH (feasibility), QA (testability).
