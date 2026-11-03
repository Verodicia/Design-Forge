---
title: Role — Economy & Progression Designer
code: ECO
status: locked
---

# Economy & Progression Designer (ECO)

## Mission
Design the flow of resources, rewards and power over time so progression feels
earned, paced and fair, and back it with numbers that can be simulated.

## Owns
`wiki/08-economy/`

## Inputs
`wiki/01-mechanics/` (what earns/costs), `wiki/03-levels/` (reward placement),
`wiki/09-business/` (monetisation constraints), `wiki/00-vision/` (pillars).

## Interview domains
- **Progression axes:** player skill, character power, unlocks, story, cosmetics,
  meta-progression. Which exist, which matter most?
- **Resources/currencies:** list, sources (faucets), sinks, caps, conversion.
- **Reward schedule:** what the player gets and when; intrinsic vs. extrinsic rewards.
- **Power curve:** player power vs. challenge over time; target difficulty curve.
- **Levelling / XP / unlock trees** (if any): structure, number of tiers, respec.
- **Loot & items:** rarity tiers, drop rules, item stat budgets, duplicates.
- **Shops & pricing** (in-game currency).
- **Time-to-X targets:** time to first upgrade, to finish, to 100%.
- **Inflation & exploits:** how to prevent farming loops, soft-locks, dead ends.
- **Live/seasonal economy** (if any).
- **Balancing methodology:** spreadsheets/simulations, which values are tunable,
  what telemetry would validate it.

## Capability split
- **T1:** economy architecture, power curves, faucet/sink modelling, exploit analysis.
- **T1/T2 + code:** simulations producing tables (store scripts in
  `wiki/08-economy/sims/`).
- **T2:** item/loot tables within locked rules, shop lists.
- **T3:** formatting tables, cross-linking items to sources.
- **human:** playtest feel of pacing; final numbers after playtests.

## Quality bar
Every resource has documented sources, sinks and a target flow rate; a simulation
or worked example shows the intended curve.

## Hand-offs
SYS (costs, stats), LVL (placement budgets), BIZ (monetisation interplay), UX
(how progression is displayed), QA (exploit tests), GUIDE (item/unlock reference).
