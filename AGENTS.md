# AGENTS.md — Start Here (Mandatory for every AI agent)

You are working inside **Design Forge**, a platform for building game design wikis
("design bibles") through structured interviews with a human Creative Owner.
Each game lives in `projects/<slug>/`. The platform rules live in `platform/`.

**Your job is never to invent the game.** Your job is to *extract* the Creative
Owner's intent through precise questions, convert answers into **locked, absolute
decisions**, and write those decisions into the wiki so that any other agent
(or human) can build the game — and eventually a player guide — from it.

---

## 1. Boot sequence (do this every session, in order)

1. Read this file completely.
2. Read [`platform/PHILOSOPHY.md`](platform/PHILOSOPHY.md) — the non-negotiable rules.
3. Read [`platform/CAPABILITIES.md`](platform/CAPABILITIES.md) and **declare your tier
   and capability flags** (see §3). If unsure, assume the *lower* tier.
4. Identify the project: ask the human, or read `projects/*/PROJECT.md`.
5. Read `projects/<slug>/PROJECT.md` and `projects/<slug>/BOARD.md`.
6. Pick a role from [`platform/roles/`](platform/roles/) (or accept the one assigned
   to you) and read that role file in full.
7. Get work: `python3 tools/forge.py next <slug> --tier <T1|T2|T3> [--role <role>]`
   (or read `projects/<slug>/tasks/` manually and apply the claim rules in
   [`platform/protocols/TASKS.md`](platform/protocols/TASKS.md)).
8. Claim exactly **one** task, do it, hand it off, then repeat from step 7.

## 2. The four protocols you must follow

| Protocol | File | When |
|---|---|---|
| Tasks | [`platform/protocols/TASKS.md`](platform/protocols/TASKS.md) | Claiming, doing, finishing, splitting work |
| Questions | [`platform/protocols/QUESTIONS.md`](platform/protocols/QUESTIONS.md) | Any time you need the Creative Owner's input |
| Decisions | [`platform/protocols/DECISIONS.md`](platform/protocols/DECISIONS.md) | Turning answers into locked facts |
| Writing | [`platform/protocols/WRITING.md`](platform/protocols/WRITING.md) | Every page you create or edit |

Also: [`platform/WORKFLOW.md`](platform/WORKFLOW.md) explains the whole lifecycle,
from a one-line seed to a finished guide.

## 3. Know your limits (capability gate)

Before claiming a task, compare its `tier` and `needs` frontmatter with your own.
- Your tier must be **equal or higher** than the task's tier (T1 > T2 > T3).
- You must have **every** capability listed in `needs`.
- If you can't meet them: **do not attempt the task.** Leave it, or, if you
  believe it is mis-tiered, add a note under `## Log` explaining why.
- If mid-task you realise it exceeds you: set `status: blocked`, write
  `blocked_reason: capability`, describe exactly where you got stuck, and stop.
  Stopping honestly is a success. Producing confident garbage is a failure.

## 4. Hard rules (summary — full list in PHILOSOPHY.md)

1. **The Creative Owner decides. You propose.** Never mark a decision `locked`
   unless it traces back to an answer from the Creative Owner (or an explicit
   delegation: "you decide").
2. **No hedging in locked content.** "Maybe / could / possibly / TBD" are banned
   in `status: locked` pages. Unknowns go in a question, not in prose.
3. **One source of truth.** Every fact lives in exactly one page; everything else
   links to it.
4. **Stay in your lane.** Only edit files your role owns. To change another
   discipline's page, open a task or question for that role.
5. **Leave a trail.** Every task has a `## Log`. Every decision has a source.
6. **Run the validator** before finishing: `python3 tools/forge.py validate <slug>`.
7. **Never edit `platform/`, `tools/` or `projects/_template/` inside a game repo**
   (a repo containing `.forge-game`). Platform changes are made in the clean base
   repo and pulled into games with `forge.py upgrade`. If you think the platform
   needs a change, tell the human. In the clean base, never create game projects.

## 5. Repository map

```
AGENTS.md                 ← you are here
README.md                 ← human overview
CHANGELOG.md              ← platform version history
.forge-game               ← present ONLY in game repos (absent = clean base)
platform/                 ← the rules (do not edit unless your task says so)
  PHILOSOPHY.md           ← core principles
  WORKFLOW.md             ← lifecycle: seed → discovery → decomposition → lock → guide
  CAPABILITIES.md         ← model tiers & capability flags
  protocols/              ← TASKS, QUESTIONS, DECISIONS, WRITING
  roles/                  ← one file per simulated team member
  templates/              ← blank task / question / decision / page files
projects/
  _template/              ← copied for every new game (do not edit for a game)
  <slug>/                 ← one folder per game
    PROJECT.md            ← seed, status, phase, owner preferences
    BOARD.md              ← generated dashboard (do not hand-edit)
    wiki/                 ← the design bible, one folder per discipline
    decisions/            ← locked decision records (D-*)
    questions/open/       ← question batches waiting for the Creative Owner
    questions/answered/   ← answered batches (archived, never deleted)
    tasks/                ← task files (T-*)
    guide/                ← the player guide, compiled from locked pages
tools/forge.py            ← CLI: spawn, upgrade, sync, new, board, next, claim, id, create, decompose, validate, guide
```
