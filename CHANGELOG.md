# Changelog — Design Forge platform

Version lives in [platform/VERSION](platform/VERSION). Use semantic versioning:
- **MAJOR**: protocol/frontmatter changes that existing projects must migrate to
  (document the migration steps here).
- **MINOR**: new roles, coverage rows, CLI commands, templates (`forge.py sync` applies them).
- **PATCH**: wording fixes, bug fixes.

Every change to `platform/`, `projects/_template/` or `tools/` gets an entry.

## 1.0.0 — 2026-11-03
- Initial platform: philosophy, workflow, capability tiers, four protocols
  (tasks, questions, decisions, writing), 15 roles, templates.
- Project template with 13 disciplines and 181 coverage items.
- `forge.py`: new, list, board, next, claim, id, create, decompose, validate, guide,
  spawn, upgrade, sync.
- Multi-product model: clean base repo + one game repo per product with the base
  as `upstream`.
