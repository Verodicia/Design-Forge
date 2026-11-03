---
title: Capability Registry
status: locked
---

# Capability Registry

Every task declares the **minimum tier** and **capability flags** it needs. Every
agent declares its own at boot. An agent may only claim tasks it meets.

> Update the *Model examples* column as new models appear. The tier definitions
> themselves are stable. When unsure which tier you are, pick the lower one.

## Tiers

| Tier | Name | Model examples (as of writing) | Trusted for | Not trusted for |
|---|---|---|---|---|
| **T1** | Frontier | Claude Opus-class, Gemini Pro-class, GPT-5-class reasoning models | Decomposing a project, designing interlocking systems, game-wide consistency review, balancing maths, architecture, writing high-stakes question batches, resolving conflicts between disciplines | Nothing on the list, but expensive: don't waste on T3 work |
| **T2** | Capable | Claude Sonnet-class, Gemini Flash-class, GPT-4.1/mini-class | Designing a single system or feature in depth, writing spec pages from locked decisions, drafting question batches inside one discipline, content lists (enemies, items, levels) within an existing framework | Game-wide decomposition, cross-discipline conflict resolution, final consistency sign-off, economy maths across many systems |
| **T3** | Light | Claude Haiku-class, Gemini Flash-Lite-class, small local models | Formatting, transcribing chat answers into question files, answer intake for simple batches, link fixing, glossary entries, filling tables from locked data, regenerating BOARD, guide assembly | Any design judgement, writing new questions, proposing decisions, anything that requires holding more than ~3 pages in mind |

**Rule:** a higher tier may take a lower-tier task; never the reverse.

## Capability flags (`needs:` in task frontmatter)

| Flag | Meaning | Typical tasks |
|---|---|---|
| `web` | Can search / browse the internet | Market research, competitor analysis, reference gathering, platform requirements |
| `code` | Can run commands and write/execute code | Running `forge.py`, prototypes, balancing simulations, data validation |
| `image-gen` | Can generate images | Mood boards, concept sketches, UI mock-ups |
| `image-read` | Can view and interpret images | Reviewing concept art or screenshots from the Creative Owner |
| `long-context` | Can reliably hold 100k+ tokens of wiki in context | Whole-wiki consistency review, guide compilation, decomposition |
| `human` | **Requires the Creative Owner or a human tester** | Game feel, playtesting, audio mixing approval, final art approval, legal/business sign-off |

## Things no model should pretend to do
Tag these `needs: [human]`. Agents prepare everything around them (checklists,
options, test scripts), but a human produces the verdict:

- Judging **game feel** (input latency, "juiciness", weight, fun).
- Judging **audio** quality, mix, or music emotionally.
- Final **aesthetic approval** of art, even when an agent generated it.
- **Playtesting** a build and reporting real player behaviour.
- **Legal, rating, licensing, and financial** commitments.
- Deciding the **vision** (pillars, fantasy, tone). Agents only propose.

## Declaring yourself (put this at the top of every task log entry)

```
agent: <model name or "unknown">  tier: T2  caps: [code, image-read]  role: systems-designer
```

## Escalation ladder
1. Task too hard → `status: blocked`, `blocked_reason: capability`, notes on where.
2. Orchestrator (T1) re-tiers or splits the task into smaller pieces a lower tier
   can handle, **or** leaves it for a T1 agent.
3. If no agent can do it (needs `human`), it becomes a question or playtest request.
