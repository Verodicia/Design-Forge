---
title: Design Forge Philosophy
status: locked
---

# Design Forge Philosophy

Design Forge borrows from classic game studios, where a **design bible** was the
single document every artist, programmer, designer and tester worked from. Ours is
written by a simulated team of AI agents, each a specialist, who **interview the
Creative Owner** until there is nothing left to guess.

## The ten principles

### 1. The Creative Owner owns the vision
Only the human Creative Owner decides what the game *is*. Agents are expert
interviewers, analysts and writers. An agent may **recommend** an answer (and
should, with reasons), but a recommendation only becomes a decision once the
Creative Owner accepts it, or explicitly delegates ("your call", "use your
recommendation"). Delegated decisions are recorded as `source: delegated`.

### 2. Absolute answers
The point of the wiki is to remove ambiguity. A locked page says **what is true**:
"The player has 3 hearts." Not "the player might have around 3 hearts."
If something is unknown it is a **question**, not a sentence. If something is
intentionally flexible, the page states the exact range and who may tune it
("Jump height: 2.0–2.4 m, tunable by Balancing during playtest").

### 3. Start small, decompose until done
Every project begins as a **seed** (one paragraph). The Orchestrator breaks it into
discipline topics, topics into tasks, and tasks into smaller tasks, until each one
can be answered by a few questions. Work is finished when every item on every
**coverage map** is `locked` or explicitly `n/a` (with a decision explaining why).

### 4. Coverage maps prevent skipped essentials
Every discipline folder has an `index.md` with a **coverage map**: the checklist of
topics a blockbuster-quality game must have answered in that discipline. Agents can
**add** items to a coverage map; they may only **remove** one through a decision
record marking it `n/a`. This is how we avoid quietly skipping essentials.

### 5. Know your capability, respect your limits
Every task carries a required **tier** and **capability flags**
(see [CAPABILITIES.md](CAPABILITIES.md)). Agents check these before claiming.
Some things no model can do on its own (judge game feel, hear a mix, playtest a
build). These are tagged `needs: [human]` and become questions or playtest tasks for
the Creative Owner, never guesses.

### 6. Questions are a product, not an interruption
Questions are carefully crafted, batched, and prioritised (see
[protocols/QUESTIONS.md](protocols/QUESTIONS.md)). Good questions offer concrete
options, explain the trade-offs, give a recommendation, and say what the answer
will unlock. The Creative Owner's time is the scarcest resource on the project.

### 7. One source of truth
Each fact lives in exactly one page, owned by one role. Other pages link to it.
If two pages disagree, the newer locked decision record wins, and the Reviewer
opens a task to fix the loser.

### 8. Traceability
Every locked statement can be traced: page → decision record (`D-*`) → answered
question (`Q-*`) → the Creative Owner's words. If you can't trace it, it isn't locked.

### 9. Lanes, not silos
Each role owns specific folders. Roles collaborate through **tasks, questions and
links**, never by silently editing each other's pages. Cross-discipline issues
(e.g. a mechanic that breaks the economy) become tasks tagged for both roles.

### 10. Write for the guide from day one
Every player-facing fact is tagged `guide: true`. When the game is finished, the
Guide Writer compiles these into a player guide. If the wiki is complete, the
guide writes itself; if the guide has holes, the wiki has holes.

## Status vocabulary (used everywhere)

| Status | Meaning |
|---|---|
| `stub` | Exists only as a placeholder / coverage item |
| `exploring` | Questions are out; answers not yet in |
| `draft` | Written from answers, awaiting Creative Owner confirmation or review |
| `locked` | Confirmed. Absolute. Changing it requires a new decision record |
| `n/a` | Deliberately out of scope, backed by a decision record |
| `superseded` | Replaced by a newer decision; kept for history |

## What "blockbuster quality" means here
We do not cut a discipline because the game is small. A tiny game still needs
answers on accessibility, audio, onboarding, save behaviour, failure states,
and so on. The answer may be short ("No save system: sessions last 5 minutes"),
but it must be **an answer**.
