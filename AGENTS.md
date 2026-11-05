# AGENTS.md

Shared engineering instructions for people and coding agents on `ai-devkit`.
Portable: no host-specific paths, no required agent, model or provider. See
[README.md](README.md) and the
[ADR](docs/explanation/decisions/0001-minimal-devkit.md).

## Engineering philosophy

- Reuse established libraries and maintained tools.
- Prefer configuration over custom infrastructure.
- Keep architecture proportional to project complexity.
- Avoid unnecessary abstractions.
- Give each concern one authoritative owner and clear boundaries.
- Make small, focused changes; read relevant code first.
- Load only the context the task needs; link to canonical documentation instead
  of copying it.

## Development workflow

- Follow the [approved implementation plan](docs/plans/ai-devkit-v0.1.md).
- Keep changes limited to the current task.
- OpenSpec will own specifications and change checklists once integrated; until
  then, the plan defines scope.
- Prefer deterministic testing and validation.
- Keep documentation synchronized with implementation.
- Never report unexecuted checks as passed.
- `mise run check` is a **planned** verification interface for generated projects;
  it does not exist in this repository yet.

## Definition of Done

A task is complete when:

- the requested behavior is implemented;
- the appropriate checks pass;
- relevant documentation and specifications are updated;
- important architectural decisions are documented in an ADR;
- no unrelated changes, secrets or merge conflicts are introduced;
- verification results and limitations are reported.

## Security

- Never commit credentials or authentication tokens.
- Never print or copy sensitive authentication material.
- Do not modify global agent configuration without explicit authorization.
- Do not weaken sandboxing or execution permissions.
- Verification commands must not modify tracked source files.

## Architectural boundaries

The project does not include:

- a custom orchestrator;
- a custom task-management system;
- a custom LLM gateway;
- a universal agent framework;
- duplicate configuration ownership for one concern;
- a hard dependency on a specific coding agent, model or provider.

Defaults are configuration, not requirements; shared standards must outlive them.
