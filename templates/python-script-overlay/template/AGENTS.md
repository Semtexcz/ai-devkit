# AGENTS.md

Engineering instructions for people and coding agents working on this project.

## Reuse first

1. Reuse a maintained tool that already solves the problem.
2. Configure it through its native configuration.
3. Extend it only where the maintained behavior stops.
4. Build only what is specific to this project.

Prefer the standard library and the dependencies already installed. Add a
dependency only when it removes more code than it adds, and record it with
`uv add` so `pyproject.toml` and `uv.lock` stay in step.

## Ownership

| Concern | Owner |
|---|---|
| Python interpreter, uv and other tool versions, tasks | `mise.toml` |
| `pyproject.toml`, `uv.lock`, `.venv/`, `main.py` | uv and this project |
| `AGENTS.md`, checker configuration, documentation seeds | the Copier overlay |
| Application behavior | you |

Work through mise so the pinned versions apply: `mise run <task>` or
`mise exec -- uv ...`. Do not add a `.python-version` file; `mise.toml` is the
single statement of the required interpreter.

## Small, testable changes

- Read the relevant code before editing it.
- Keep one change reviewable on its own; do not mix a refactor with a behavior
  change.
- Cover every behavior change with a test. Keep the existing smoke test
  meaningful rather than decorative.
- Never weaken a check, delete a test or add a skip to obtain a passing result.

## Documentation

- Update the page that describes what changed, or state why no page needs to.
- Keep the documentation link-clean: `mise run docs` fails on a broken internal
  link.
- Record a significant decision as a short page under `docs/explanation/`.

## Definition of Done

A change is complete when:

- the requested behavior works;
- `mise run check` passes;
- tests cover the new behavior;
- documentation reflects the change;
- the diff contains no secrets, unrelated changes or unresolved conflicts.

## Security

- Never commit credentials, tokens or private keys. Local secrets belong in
  `.env`, which Git ignores.
- `AGENTS.md` is guidance, not a sandbox. Review the commands an agent proposes,
  especially anything destructive, privileged or network-facing.
- Do not run `sudo`, rewrite Git history or push without an explicit request.

## Verify

`mise run check` is the canonical verification command. It runs the locked
dependency check, Ruff lint and format check, `mypy --strict`, pytest and the
strict documentation build. See `docs/reference/commands.md` for the individual
tasks.
