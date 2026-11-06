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
- OpenSpec owns behavioral requirements and change task lists. Specs live in
  `openspec/specs/`, proposed changes in `openspec/changes/`; both are written and
  validated by the native CLI (`openspec new change`, `openspec validate`,
  `openspec archive`). Do not create a backlog, task-state file or workflow schema
  next to them.
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
- `mise run test-template` is the generation integration test. It needs the package
  index and is therefore kept out of `check`; run both before reporting a change
  that touches the overlay.

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
