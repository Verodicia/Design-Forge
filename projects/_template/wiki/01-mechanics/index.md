---
title: Mechanics & Systems
owner: systems-designer
status: stub
guide: false
decisions: []
coverage: 01-mechanics/index
updated: {{DATE}}
---

# Mechanics & Systems

**Owner:** [systems-designer](../../../../platform/roles/systems-designer.md) (`SYS`)

How the game plays. Every page must pass the programmer test: zero ambiguity.

## Coverage map

Every row must reach `locked` or `n/a` (with a decision). Add rows for anything this game needs that is missing. Remove rows only via an `n/a` decision. `tier`/`needs`/`phase` are defaults used by `forge.py decompose`.

| key | topic | tier | needs | phase | status | page | ref |
|---|---|---|---|---|---|---|---|
| `core-loop` | Core loop at moment / minute / session scale | T1 |  | 3 | stub | | |
| `verbs` | Complete player verb list (input, conditions, outcome, cost, feedback) | T1 |  | 3 | stub | | |
| `controls` | Control scheme per platform and device | T2 |  | 3 | stub | | |
| `camera` | Camera behaviour | T2 |  | 3 | stub | | |
| `avatar` | Player character model: stats and state machine | T1 |  | 3 | stub | | |
| `movement` | Movement system | T2 |  | 3 | stub | | |
| `time-structure` | Real-time vs turn-based, pausing, in-game time | T2 |  | 3 | stub | | |
| `challenge-model` | What opposes the player | T1 |  | 3 | stub | | |
| `conflict-system` | Combat / primary conflict system | T1 |  | 3 | stub | | |
| `enemies-ai` | Enemy and NPC behaviour | T2 |  | 4 | stub | | |
| `abilities` | Abilities, skills, powers | T2 |  | 4 | stub | | |
| `failure-states` | Failure, death, retry and their costs | T1 |  | 3 | stub | | |
| `win-conditions` | Win conditions and completion | T1 |  | 3 | stub | | |
| `difficulty` | Difficulty model, modes and assists | T1 |  | 3 | stub | | |
| `systems-catalogue` | Catalogue of secondary systems (one page each) | T1 |  | 3 | stub | | |
| `system-interactions` | Systemic interaction matrix and intended emergence | T1 |  | 4 | stub | | |
| `randomness` | Randomness: where, distributions, bad-luck protection | T2 |  | 4 | stub | | |
| `persistence` | What persists across sessions, runs, deaths | T2 |  | 3 | stub | | |
| `game-modes` | Game modes | T2 |  | 3 | stub | | |
| `multiplayer` | Multiplayer and social rules | T1 |  | 3 | stub | | |

## Pages

<!-- Link each page here as it is created. -->
