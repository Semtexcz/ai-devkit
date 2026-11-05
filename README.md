# ai-devkit

`ai-devkit` is a portable, versioned collection of development configurations,
engineering rules, documentation and a small project overlay. It composes
maintained tools rather than implementing a development framework.

It targets developers building small Python applications and scripts with coding
agents who want reproducible toolchains and explicit standards.

## Philosophy: Reuse → Configure → Extend → Build

1. **Reuse** a maintained tool that already solves the problem.
2. **Configure** it through its native configuration.
3. **Extend** it only where the maintained behavior stops.
4. **Build** only project-specific policy.

Custom code is the last resort.

## Status

This commit is documentation only: no tooling, template, CI workflow or agent
configuration exists yet, and nothing here is verified as working. Implemented:
this README, `AGENTS.md`, `.gitignore` and the ADR. Planned work is tracked in the
[approved implementation plan](docs/plans/ai-devkit-v0.1.md).

## Intended v0.1 architecture and stack

| Concern | Planned tool |
|---|---|
| Tool versions, tasks | mise |
| Python envs, dependencies, lockfiles | uv |
| Initial scaffold | native `uv init` |
| Standards/docs overlay | Copier |
| Specs and change checklists | OpenSpec |
| Routine coding | OpenCode + DeepSeek |
| Advanced coding | Codex CLI + ChatGPT auth |
| Agent instructions | AGENTS.md |
| Python quality | Ruff, mypy, pytest |
| Documentation | Diátaxis, Zensical |
| CI | GitHub Actions |

## Initial focus

The only v0.1 profile is an **unpackaged Python application or script**: a
runnable entry point, one smoke test, linting, type checking and documentation.
Packaging, publishing, containers, extra profiles and orchestration are deferred.

## Independence from `_ai_project_template`

`ai-devkit` is independent of `_ai_project_template`: it keeps that project's
emphasis on small slices, executable checks and explicit ownership, but replaces
its policy resolver, context router and lifecycle with native configuration. No
code is shared.

## Documentation

- [AGENTS.md](AGENTS.md) — engineering rules for agents and humans.
- [ADR 0001](docs/explanation/decisions/0001-minimal-devkit.md) — design rationale.
- [ai-devkit v0.1 plan](docs/plans/ai-devkit-v0.1.md) — scope and backlog.
