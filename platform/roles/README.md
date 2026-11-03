---
title: Team Roster
status: locked
---

# Team Roster

Each role is a simulated specialist. An agent **adopts one role per task**. Role
files define what the role owns, how it interviews the Creative Owner, and how it
splits work to fit agent capabilities.

| Code | Role | File | Owns | Lead tier | Phase focus |
|---|---|---|---|---|---|
| ORC | Orchestrator | [orchestrator.md](orchestrator.md) | `PROJECT.md`, `tasks/` structure, phase gates | T1 | All |
| REV | Reviewer / Continuity Editor | [reviewer.md](reviewer.md) | `wiki/glossary.md`, consistency audits | T1 | 3–5 |
| CD | Creative Director | [creative-director.md](creative-director.md) | `wiki/00-vision/` | T1 | 1–2 |
| SYS | Systems Designer | [systems-designer.md](systems-designer.md) | `wiki/01-mechanics/` | T1 | 2–4 |
| NAR | Narrative Designer | [narrative-designer.md](narrative-designer.md) | `wiki/02-narrative/` | T1/T2 | 2–4 |
| LVL | Level Designer | [level-designer.md](level-designer.md) | `wiki/03-levels/` | T2 | 3–4 |
| ART | Art Director | [art-director.md](art-director.md) | `wiki/04-art/` | T2 | 2–4 |
| AUD | Audio Director | [audio-director.md](audio-director.md) | `wiki/05-audio/` | T2 | 3–4 |
| UX | UX/UI & Accessibility Designer | [ux-designer.md](ux-designer.md) | `wiki/06-ux/` | T2 | 3–4 |
| TECH | Technical Director | [technical-director.md](technical-director.md) | `wiki/07-tech/` | T1 | 1–4 |
| ECO | Economy & Progression Designer | [economy-designer.md](economy-designer.md) | `wiki/08-economy/` | T1 | 3–4 |
| BIZ | Business Strategist | [business-strategist.md](business-strategist.md) | `wiki/09-business/` | T1/T2 | 1–4 |
| PROD | Producer | [producer.md](producer.md) | `wiki/10-production/` | T1/T2 | 1, 6 |
| QA | QA Lead | [qa-lead.md](qa-lead.md) | `wiki/11-qa/` | T2 | 4–5 |
| GUIDE | Guide Writer | [guide-writer.md](guide-writer.md) | `wiki/12-guide-plan/`, `guide/` | T2 | 5–6 |

"Lead tier" is the tier for the role's *design* work (decomposition, interviews,
cross-checks). Every role has plenty of T2/T3 sub-work; each role file lists it.

## Shared rules for every role
- Read your role file **and** your discipline's `index.md` coverage map before working.
- Interview topics in each role file are **starting points**. Tailor questions to
  the locked vision; never ask generic questions the vision already answers.
- Every role must look for **cross-discipline consequences** and create tasks
  for affected roles.
- If a topic doesn't apply to this game, propose `n/a` through a question; never
  just skip it.

## Role file structure
Every role file has the same sections: **Mission · Owns · Inputs (read before
working) · Interview domains · Capability split · Quality bar · Hand-offs**.
