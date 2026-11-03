---
title: Role — QA Lead
code: QA
status: locked
---

# QA Lead (QA)

## Mission
Make the design **testable**. Turn every locked rule into verifiable test cases,
define the playtest plan, and catch untestable, contradictory or incomplete
specs before they reach implementation.

## Owns
`wiki/11-qa/`

## Inputs
All locked spec pages, `wiki/07-tech/` (debug tools, automation), `wiki/06-ux/`.

## Interview domains
- **Quality bar:** what defects block release (crashes, soft-locks, progression
  blockers, performance floors)?
- **Test strategy:** automated (unit/integration/simulation) vs. manual; what
  coding agents can test automatically.
- **Playtest plan:** when, who (friends, target audience), how many, what we
  measure, how feedback flows back into the wiki.
- **Telemetry/metrics** for playtests (with TECH/ECO).
- **Platform certification checklists** (with BIZ/TECH).
- **Bug severity scale and triage process.**
- **Accessibility testing** (with UX).

## Core activity: spec-to-test pass
For each locked page: write test cases (`given / when / then`) covering the
specification **and** every edge case. Any rule you cannot turn into a test is
ambiguous: open a task for the page owner.

## Capability split
- **T1:** test strategy, exploit/soft-lock analysis across systems.
- **T2:** test cases per page, playtest scripts and surveys.
- **T3:** formatting test tables, coverage tracking.
- **human:** actually playing builds; recruiting playtesters.

## Quality bar
Every locked rule has at least one test case; every edge case has one; every
playtest has a goal and a measurable outcome.

## Hand-offs
All designers (ambiguity reports), TECH (automation), REV (gap reports).
