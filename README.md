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

Implemented and verified on Linux x86-64 (Tasks 1–2 of the
[approved implementation plan](docs/plans/ai-devkit-v0.1.md)):

- an engineering contract in `AGENTS.md` and an architecture decision record;
- a pinned toolchain: mise installs Python 3.13.18, Node.js 24.22.2, uv 0.13.7,
  OpenSpec 1.16.0, OpenCode 1.19.5 and the OpenAI Codex CLI 0.163.0 from
  `mise.lock`, with npm sidecar locks under `.mise/locks/`;
- a locked Python development environment (Copier, pytest, Ruff, mypy, Zensical)
  managed by uv in `pyproject.toml` and `uv.lock`;
- a Zensical documentation site with strict internal-link validation, exposed as
  `mise run docs`, `mise run docs-serve` and `mise run check`.

Not implemented yet: the Copier overlay, OpenSpec initialization, agent
model/provider configuration, application code and tests, and CI. Nothing else
is claimed to work.

## Quick start

Prerequisites: Linux x86-64, Git, `curl`, `tar`, CA certificates, and no need
for `sudo`.

```bash
mise trust                       # after reviewing mise.toml
mise install --locked            # runtimes and CLIs from mise.lock
mise exec -- uv sync --locked    # Python tools from uv.lock
mise run check                   # implemented checks (locked deps + strict docs)
```

mise itself is installed manually; see
[docs/tutorials/getting-started.md](docs/tutorials/getting-started.md) for the
step-by-step version, including checksum verification.

## Toolchain ownership

| Concern | Owner | Lockfile |
|---|---|---|
| Runtimes and CLI versions | mise | `mise.lock` (+ `.mise/locks/`) |
| Python environment and dependencies | uv | `uv.lock` |
| Documentation structure | Diátaxis | `docs/` |
| Documentation build | Zensical | `zensical.toml` |
| Tasks | mise | `[tasks]` in `mise.toml` |

## Intended v0.1 architecture and stack

| Concern | Tool | Status |
|---|---|---|
| Tool versions, tasks | mise | implemented |
| Python envs, dependencies, lockfiles | uv | implemented |
| Documentation | Diátaxis, Zensical | implemented |
| Python quality | Ruff, mypy, pytest | pinned, not wired into `check` yet |
| Initial scaffold | native `uv init` | planned |
| Standards/docs overlay | Copier | pinned, overlay planned |
| Specs and change checklists | OpenSpec | pinned, initialization planned |
| Routine coding | OpenCode + DeepSeek | pinned, configuration planned |
| Advanced coding | Codex CLI + ChatGPT auth | pinned, configuration planned |
| Agent instructions | AGENTS.md | implemented |
| CI | GitHub Actions | planned |

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

The documentation site uses Diátaxis and is built with Zensical
(`mise run docs`, preview with `mise run docs-serve`). Entry point:
[docs/index.md](docs/index.md).

- [Getting started](docs/tutorials/getting-started.md) — install the toolchain and build the docs.
- [Install the development toolchain](docs/how-to/install-toolchain.md) — install, update, roll back.
- [Tool ownership and pinned versions](docs/reference/tool-versions.md) — the tested version tuple.
- [Reproducibility and Python ownership](docs/explanation/reproducibility.md) — why mise and uv are separate.
- [ADR 0001](docs/explanation/decisions/0001-minimal-devkit.md) — design rationale.
- [ai-devkit v0.1 plan](docs/plans/ai-devkit-v0.1.md) — scope and backlog.
- [AGENTS.md](AGENTS.md) — engineering rules for agents and humans.
