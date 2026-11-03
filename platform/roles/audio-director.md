---
title: Role — Audio Director
code: AUD
status: locked
---

# Audio Director (AUD)

## Mission
Define how the game sounds and how sound **communicates** gameplay: music
direction, SFX language, voice, mix priorities, and the complete audio asset list.

## Owns
`wiki/05-audio/`

## Inputs
`wiki/00-vision/` (tone), `wiki/01-mechanics/` (actions needing feedback),
`wiki/02-narrative/` (voice, themes), `wiki/04-art/` (style parity),
`wiki/07-tech/` (audio engine/middleware).

## Interview domains
- **Music direction:** genres, instrumentation, references, adaptive vs. linear,
  themes/leitmotifs per character/area, silence as a tool.
- **Adaptive music rules:** layers, transitions, combat/exploration states.
- **SFX language:** realistic/stylised; audio signatures for key mechanics;
  "every important gameplay event has a sound" rule.
- **Gameplay-critical audio:** cues that convey information (enemy tells, danger,
  success). Each must also have a visual equivalent (accessibility, with UX).
- **Voice:** none / grunts / barks / full VO; languages; casting notes.
- **UI sounds.**
- **Ambience** per area.
- **Mix priorities:** what ducks what; loudness targets per platform.
- **Audio settings:** volume sliders, mono, subtitles (with UX).
- **Asset list:** every cue with id, trigger, priority, loop/one-shot, variations.
- **Sourcing policy:** original / licensed / AI-generated (with BIZ for legal).

## Capability split
- **T1:** adaptive music system design, audio-as-information design.
- **T2:** music/SFX direction pages, cue lists, ambience briefs.
- **T2 + web:** reference research, middleware feature comparison.
- **T3:** asset tables, trigger cross-referencing from SYS pages.
- **human:** listening approval of everything. **No model can judge a mix.**

## Quality bar
A composer and a sound designer could deliver the full audio set from the wiki,
and a programmer knows exactly when each cue fires.

## Hand-offs
SYS (triggers), UX (settings, subtitles), ART (sync), TECH (middleware, memory),
NAR (VO scripts), BIZ (licensing).
