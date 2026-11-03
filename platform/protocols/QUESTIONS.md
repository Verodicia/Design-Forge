---
title: Question Protocol
status: locked
---

# Question Protocol — How to Grill the Creative Owner

Questions are how the game gets designed. Treat each one as a crafted product.

## Where questions live
- `projects/<slug>/questions/open/Q-<ROLECODE>-<NNNN>.md`: waiting for answers.
- `projects/<slug>/questions/answered/`: answered and processed. **Never delete.**
- ID: `python3 tools/forge.py id <slug> question <ROLECODE>`.

## Who may write questions
- Writing **new** questions requires **T2 or higher** in the owning role.
- Questions that span disciplines or touch the vision require **T1**.
- T3 agents may only **transcribe** answers and run intake.

## The anatomy of a good question

```markdown
### Q3. How does the player recover health?
**Why it matters:** Determines pacing of combat encounters and whether
consumables exist in the economy.
**Options:**
- **A) Regenerates over time out of combat.** Fast pacing, fewer resources to
  manage, less tension.
- **B) Consumable items only.** Tension and resource management; requires an
  item economy (affects 08-economy).
- **C) Checkpoints restore health.** Simple; makes each segment a self-contained
  challenge.
- **D) Other.** Describe.
**Recommendation:** B, because pillar P2 "every resource is a choice" (D-CD-0003).
**Unlocks:** T-SYS-0011 (combat pacing), T-ECO-0004 (consumables).
**Your answer:**
>
```

Rules:
1. **One decision per question.** No compound "and/or" questions.
2. **Concrete options** (2–5) plus "Other". Open-ended questions are allowed only
   in Discovery (Phase 0–1) for vision topics, and must include example answers.
3. **State trade-offs**, not just labels.
4. **Always recommend**, and cite the pillar/decision behind it. Be honest when
   you have no basis: "No recommendation; this is pure taste."
5. **Say what it unlocks**, so the Creative Owner sees the value.
6. **Never ask what is already locked.** Search `decisions/` first.
7. **Never ask what you can find out yourself** (genre conventions, platform
   specs, competitor facts). Research it and present it as context instead.
8. **Use plain language.** Define any jargon inline.
9. **Respect the Creative Owner's batch preferences** in `PROJECT.md`
   (default: 5–7 questions per batch, ordered most- to least-important).
10. **Allow delegation.** Every batch ends with: *"For any question, you may reply
    'your call' to accept the recommendation."*

## Batch frontmatter

```yaml
---
id: Q-SYS-0002
title: Health and damage fundamentals
role: systems-designer
status: open          # open | answered | processed
priority: high        # blocking | high | normal | low
tasks: [T-SYS-0011]   # tasks waiting on this batch
created: 2026-11-03
---
```

## Answering (Creative Owner)
Write answers under each `**Your answer:**` line: a letter ("B"), "your call",
or free text. Then set `status: answered`. Or answer in chat; an agent will
transcribe your words **verbatim** into the file.

## <a id="intake"></a>Answer intake (any agent T3+, T2+ if answers are free-text and ambiguous)
1. For each answered question, create a decision record ([DECISIONS.md](DECISIONS.md)).
   - Letter answer → decision = that option. `source: owner`.
   - "your call" → decision = recommendation. `source: delegated`.
   - Free text that is **ambiguous** → do **not** guess. Write a follow-up
     question in a new batch referencing the original.
2. Set batch `status: processed`, move the file to `questions/answered/`.
3. For each task in `tasks:` → set `status: open`, add a log line.
4. Run `forge.py board <slug>`.

## Priorities
- `blocking`: other disciplines can't progress; ask now.
- `high`: needed for the current phase.
- `normal`: needed before the phase exits.
- `low`: polish/detail; can wait for a quiet batch.

The Orchestrator may merge several roles' small batches into one session so the
Creative Owner isn't flooded. Check `PROJECT.md → owner_preferences` before sending.
