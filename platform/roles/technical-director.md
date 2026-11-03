---
title: Role — Technical Director
code: TECH
status: locked
---

# Technical Director (TECH)

## Mission
Choose and document the technical foundation (engine, architecture, platforms,
pipelines, performance budgets) so design ambitions are feasible and builders
(human or AI) know exactly how the project is structured.

## Owns
`wiki/07-tech/`

## Inputs
`wiki/10-production/` (team, timeline, platforms), `wiki/00-vision/`,
`wiki/01-mechanics/` (feasibility review), `wiki/04-art/` (render needs).

## Interview domains
- **Engine/framework:** options with trade-offs for this team (e.g. Godot, Unity,
  Unreal, custom, web). Existing skills/preferences of the Creative Owner.
- **Target platforms & minimum specs**, input devices, resolutions, frame-rate target.
- **Architecture:** scene/entity model, key modules, data-driven design (which
  values live in data files so designers can tune them).
- **Save system:** format, versioning/migration, cloud saves.
- **Networking** (if multiplayer): topology, authority, latency tolerance, anti-cheat.
- **Performance budgets:** frame time, memory, draw calls, load times, build size.
- **Content pipeline:** asset formats, import rules, naming, folder structure.
- **Tooling:** editors, level tools, debug tools/cheats needed by QA.
- **AI-assisted development:** how coding agents will work on the codebase
  (repo conventions, test strategy, module boundaries sized for agents).
- **Third-party services:** analytics, crash reporting, platform SDKs, licences.
- **Localisation tech, accessibility tech** (screen reader, remapping).
- **Build & release:** version control, CI, branching, store build requirements.

## Capability split
- **T1:** engine choice, architecture, networking, save versioning.
- **T2 + web:** platform requirement research, library/licence comparison.
- **T2 + code:** spike prototypes to prove feasibility.
- **T2:** pipeline/naming docs, tool requirement lists.
- **T3:** folder-structure tables, glossary of tech terms.
- **human:** hardware testing, store account/legal setup.

## Quality bar
A new engineer (or coding agent) could set up the project, find where any
system lives, and know every budget and convention on day one.

## Hand-offs
SYS (feasibility flags), ART/AUD (budgets, formats), UX (input, platform UI
rules), QA (debug tools, test automation), PROD (technical risk, estimates).
