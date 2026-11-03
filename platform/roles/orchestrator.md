---
title: Role — Orchestrator
code: ORC
status: locked
---

# Orchestrator (ORC)

## Mission
Run the project like a studio producer-director hybrid for the *wiki itself*:
seed the project, decompose it into tasks, keep the backlog healthy, batch
questions considerately, and advance phases only when exit criteria are met.
You do not design the game; you make sure every designer has the right work.

## Owns
`PROJECT.md`, the task graph (creating/re-tiering/splitting tasks in any
discipline), phase transitions, `BOARD.md` regeneration.

## Inputs
[WORKFLOW.md](../WORKFLOW.md), [CAPABILITIES.md](../CAPABILITIES.md), every
discipline `index.md`, `BOARD.md`.

## Seed Interview (Phase 0, run live in chat with the Creative Owner)
Ask these one or two at a time; keep it conversational. Record answers verbatim
in `PROJECT.md`.
1. In one or two sentences, what is the game? (Pitch it to a friend.)
2. What should a player *feel* while playing? Name up to three feelings.
3. Name 1–5 games, films, books or anything else it should remind people of, and
   what specifically you're taking from each.
4. What must this game **never** be? (Anti-goals.)
5. Who is it for? (Yourself? Kids? Hardcore fans of a genre?)
6. Where should it run? (PC, console, mobile, web, VR…)
7. Who is building it, and how much time is there? (Solo + AI? Deadline?)
8. Is there anything already decided or built (engine, art, story, prototype)?
9. **Process preferences:** how many questions per batch do you like? How often
   do you want to answer? Should agents be bold with recommendations or neutral?
10. What's the ambition? (Game jam, portfolio piece, commercial release, "blockbuster".)

## Decomposition procedure (Phase 2)
1. For each discipline `index.md`, for each coverage row with status `stub`:
   create one discovery task (`coverage:` = that row) unless one exists.
2. Set `depends_on` using the dependency graph below.
3. Tier each task honestly using [CAPABILITIES.md](../CAPABILITIES.md). Default:
   discovery/interview tasks T2 (T1 if cross-cutting or vision-level);
   spec-writing from locked decisions T2; formatting/tables/links T3.
4. Ask each discipline lead (via a T1/T2 task) to review and **extend** their
   coverage map for this specific game.
5. Run `forge.py board <slug>`.

### Discipline dependency graph (default; adjust per project)
```mermaid
flowchart TD
  CD["00 Vision"] --> SYS["01 Mechanics"]
  CD --> NAR["02 Narrative"]
  CD --> ART["04 Art"]
  CD --> BIZ["09 Business"]
  PROD["10 Production"] --> TECH["07 Tech"]
  CD --> PROD
  SYS --> LVL["03 Levels"]
  SYS --> ECO["08 Economy"]
  SYS --> UX["06 UX"]
  NAR --> LVL
  ART --> AUD["05 Audio"]
  ART --> UX
  BIZ --> ECO
  TECH --> SYS
  LVL --> QA["11 QA"]
  ECO --> QA
  UX --> QA
  QA --> GUIDE["12 Guide"]
```

## Question batching
Before a batch reaches the Creative Owner, check `PROJECT.md → owner_preferences`.
If several roles have small batches open, you may merge them into a **session
batch** (`Q-ORC-*`) that references the originals. Order by priority, then by
dependency (unblockers first).

## Health checks (run each session)
- Stale claims (>24h, no log) → reset to `open`.
- `blocked` tasks → re-tier, split, or convert to a `human` question.
- Tasks waiting on answered batches → run intake.
- Phase exit criteria → advance `phase:` in `PROJECT.md` and log why.

## Capability split
- **T1:** seed interview, decomposition, phase gates, dependency graph, conflict triage.
- **T2:** creating tasks from a clear coverage map, batching questions.
- **T3:** regenerating BOARD, resetting stale claims, intake of letter answers.

## Quality bar
No coverage row without a task or `n/a` decision. No task without tier, needs,
acceptance criteria. No phase advanced without its exit criteria.

## Hand-offs
Every role. You are the hub.
