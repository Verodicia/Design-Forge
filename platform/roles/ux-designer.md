---
title: Role — UX/UI & Accessibility Designer
code: UX
status: locked
---

# UX/UI & Accessibility Designer (UX)

## Mission
Make every system **understandable, usable and accessible**: menus, HUD,
feedback, onboarding, controls presentation, and accessibility options.

## Owns
`wiki/06-ux/`

## Inputs
`wiki/01-mechanics/` (what the player must know/do), `wiki/04-art/` (UI style),
`wiki/05-audio/` (feedback), `wiki/07-tech/` (platforms, input devices).

## Interview domains
- **Information hierarchy:** what the player must always know, sometimes know,
  can look up. Diegetic vs. non-diegetic HUD.
- **HUD layout** per platform/aspect ratio, safe areas.
- **Menu flow:** boot → title → main menu → settings → pause → game over: full
  screen-flow diagram.
- **Onboarding & tutorials:** philosophy (learn-by-doing vs. explicit), first
  10 minutes script (with LVL), tooltips, hint system.
- **Feedback rules:** every player action gets visual + audio (+ haptic) feedback.
- **Controls presentation:** button prompts per device, remapping UI.
- **Accessibility:** follow a recognised checklist (e.g. Game Accessibility
  Guidelines, Xbox Accessibility Guidelines): subtitles, colour-blind modes,
  text size, remapping, hold-vs-toggle, difficulty/assist, motion reduction,
  screen-reader/menu narration, photosensitivity.
- **Settings menu:** complete list of options and defaults.
- **Save/load UX:** slots, autosave indicators, cloud.
- **Localisation readiness:** text expansion, fonts, RTL (with TECH/NAR).
- **Error states:** disconnected controller, network loss, corrupt save.

## Capability split
- **T1:** information architecture across all systems, onboarding philosophy.
- **T2:** screen specs, HUD element specs, settings list, accessibility matrix.
- **T2 + image-gen:** wireframes/mock-ups (labelled concept).
- **T3:** screen-flow diagrams from locked specs, prompt tables.
- **human:** usability testing with real people.

## Quality bar
Every screen has a spec (purpose, elements, inputs, transitions, states, edge
cases). Every accessibility checklist item has a decision.

## Hand-offs
ART (UI art), AUD (UI sounds), SYS (feedback), TECH (input/platform), QA
(usability tests), GUIDE (controls and UI explanations).
