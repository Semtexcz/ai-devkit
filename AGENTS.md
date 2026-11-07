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

## Product direction

- The canonical product vision is [docs/vision.md](docs/vision.md) and the
  canonical roadmap is [docs/plans/roadmap.md](docs/plans/roadmap.md). They own the
  product mission, the target capabilities, the ownership boundaries and the
  milestones; no other file restates them.
- Every change must be architecturally consistent with the vision, including its
  ownership table: one authoritative owner per concern, reuse before extension,
  and no capability the vision assigns elsewhere. If a change would conflict with
  the vision, stop and raise it with the human instead of widening scope quietly.
- The roadmap records direction, not scope. **It does not authorize implementation
  of any milestone after v0.1.** Starting a milestone is a human decision, and its
  actionable scope is an approved OpenSpec change.
- Human authorization and an OpenSpec change record are different things. The human
  approves consequential product scope, milestone implementation and releases.
  OpenSpec is the authoritative specification and change system for behavioral
  work. A roadmap item is never implementation authorization by itself, and never
  read a future milestone as permission to begin work.
- `docs/plans/ai-devkit-v0.1.md` is historical implementation documentation for
  the implemented v0.1 baseline; it is not a live plan.

## Development workflow

- Follow the [product vision](docs/vision.md) and the [roadmap](docs/plans/roadmap.md)
  for direction, and implement only what is approved.
- Keep changes limited to the current task.
- OpenSpec owns behavioral requirements and change task lists. Specs live in
  `openspec/specs/`, proposed changes in `openspec/changes/`; both are written and
  validated by the native CLI (`openspec new change`, `openspec validate`,
  `openspec archive`). Do not create a backlog, task-state file or workflow schema
  next to them.
- Small documentation fixes, typo corrections and routine administrative
  maintenance need no OpenSpec change unless they alter behavioral requirements or
  approved scope.
- `AGENTS.md` owns engineering rules, ADRs own architectural rationale, and
  OpenSpec owns what the system must do; see
  [OpenSpec, AGENTS.md and ADRs](docs/explanation/openspec-and-agents.md).
- Prefer deterministic testing and validation.
- Keep documentation synchronized with implementation.
- Never report unexecuted checks as passed.
- Run `mise run check` before reporting a task complete.

## Toolchain and checks

- mise owns runtimes and CLI versions; uv owns the Python environment and its
  dependencies. Neither concern gets a second owner.
- `mise.toml`, `pyproject.toml` and the committed lockfiles are the sources of
  truth. Never hand-edit `mise.lock`, `.mise/locks/**` or `uv.lock`; regenerate
  with `mise lock` or `uv lock` and review the diff.
- Run tools through mise (`mise exec -- uv ...`, `mise run <task>`) so pinned
  versions and `UV_NO_MANAGED_PYTHON=1` apply.
- Do not add a `.python-version` file; mise selects the interpreter.
- Tasks: `docs` (strict build), `docs-serve`, `lock-check`, `examples-check`,
  `spec-check`, `test-template`, `check`, `versions`. Add checks to `check` only when
  the capability genuinely exists.
- `mise run check` runs `lock-check`, `examples-check`, `spec-check` and `docs`.
  `spec-check` is the native command `openspec validate --all --strict
  --no-interactive`; never replace it with a custom parser.
- A generated project's `mise run check` is a different and larger set: dependency
  lock verification, Ruff lint, Ruff formatting, `mypy`, pytest, the strict
  documentation build and OpenSpec validation. That is seven checks, not this
  repository's four; never describe one set with the other's count.
- `mise run test-template` is the generation integration and update lifecycle test.
  It needs the package index and is therefore kept out of `check`; run both before
  reporting a change that touches the overlay or the tests.
- `.github/workflows/verify.yml` runs the same commands with `contents: read` and no
  secret. Keep it that way: no write permission, no `pull_request_target`, no
  credential, no model call and no publish step. `tests/test_ci_workflow.py` guards
  those properties.

## OpenSpec integration boundary

- OpenSpec is initialized natively: `openspec init --tools opencode,codex --profile
  core`. Its generated files (`openspec/`, `.opencode/`, `.agents/`) have exactly one
  owner: OpenSpec. Never hand-edit them, never copy them from another project, and
  never render them through Copier.
- `openspec/config.yaml` carries the schema and, if needed, project rules. Model
  names, providers and credentials never appear in it.
- A generated project initializes OpenSpec itself, with the command above, and pins
  OpenSpec and Node.js in its own `mise.toml`.

## Project overlay boundary

- `copier.yml` and `templates/python-script-overlay/template/` are the only template
  source; `_subdirectory` keeps the rest of the repository out of rendered projects.
- The overlay owns policy: rules, checker configuration, documentation seeds and
  ignore rules. It must never render `main.py`, `pyproject.toml`, `uv.lock` or
  `.python-version`, because uv and the project developer own those files.
- It must also never render `openspec/`, `.opencode/`, `.agents/` or `.clinerules/`:
  OpenSpec generates those in each project, and a template copy would be a second
  owner that drifts from the pinned CLI.
- It must never render this repository's vision, roadmap or ADRs as project
  content: a generated project owns its own direction, and shipping the devkit's
  milestones into it would make provisional proposals look like project scope.
- Copier provenance is `.copier-answers.yml`, rendered by the template. Never add a
  devkit-specific version table or a custom update command.
- Do not add Copier tasks that execute commands, and do not patch application code
  from the template. The `def main() -> None:` annotation is a documented
  project-owned edit; see
  [ADR 0002](docs/explanation/decisions/0002-script-project-overlay.md).
- Never create, move or push ai-devkit release tags from an automated change. The
  integration test uses a temporary tagged repository.
- Documentation follows Diátaxis under `docs/` and builds with `--strict`, so a
  broken internal link fails the build.
- Linux x86-64 is the only verified platform. Do not claim macOS, WSL2 or
  clean-machine support without evidence.

## Agent configuration

- Harness, provider, model, execution profile, role and orchestrator are separate
  concepts. Each harness keeps its own native configuration and credential store.
- Model names, account-dependent defaults and credentials are user-level
  configuration. They never become shared engineering rules, because a shared rule
  must outlive the account and the release that made it convenient.
- Configuration examples under `examples/agents/` are credential-free and inert.
  The devkit documents and configures harnesses; it does not launch, route or
  authenticate them.
- See the [agent configuration reference](docs/reference/agent-configuration.md).

## Changelog

`CHANGELOG.md` is the only changelog. It follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning,
with an `Added`, a `Changed` and a `Fixed` section under each version.

- Decide, before reporting a task complete, whether the change affects the
  changelog, and say so either way.
- Record user-visible features, behavior changes, breaking changes, compatibility
  changes, significant toolchain changes, deprecations and important fixes under
  `[Unreleased]`.
- Do not record formatting changes, typo fixes, ordinary refactors or other work
  with no user-visible effect, and do not duplicate an entry that is already there.
  If no entry is required, state the reason in the completion report.
- When preparing a release, move the relevant entries from `[Unreleased]` into the
  new version section, date that section, and leave `[Unreleased]` in place, empty.
- Never record a speculative or unverified claim, and never describe an
  undocumented user-visible change as complete.
- Keep one canonical owner: do not add a second release history next to this file
  and do not copy the changelog into `docs/`.

Changelog maintenance is part of the Definition of Done.

## Definition of Done

A task is complete when:

- the requested behavior is implemented;
- the appropriate checks pass;
- relevant documentation and specifications are updated;
- the change is recorded in `CHANGELOG.md`, or the completion report states why no
  entry is required;
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
