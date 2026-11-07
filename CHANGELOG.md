# Changelog

Notable changes to ai-devkit are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
`AGENTS.md` states when an entry is required and when it is not; this file is the
only changelog.

## [Unreleased]

### Added

- A product vision and a reconciled roadmap.
  [docs/vision.md](docs/vision.md) records the mission, the target autonomous
  development lifecycle, the target capabilities, the human approval boundaries,
  the ownership boundaries, the non-goals and the metrics that measure progress.
  [docs/plans/roadmap.md](docs/plans/roadmap.md) reconciles the historical v0.1
  backlog with what v0.1.0 delivers and records the provisional milestones after
  it; those milestones are proposals, not approved scope, and OpenSpec remains the
  only owner of actionable changes.
- [docs/explanation/lessons-from-ai-project-template.md](docs/explanation/lessons-from-ai-project-template.md),
  an evidence-based decision matrix recording what `ai-devkit` retains, adapts,
  delegates, defers and rejects from `_ai_project_template`, with links pinned to
  the reviewed commit.
- `AGENTS.md` now points to the vision and the roadmap, requires architectural
  consistency with the vision, states that the roadmap does not authorize
  implementation of any milestone after v0.1, and forbids rendering the devkit's
  vision, roadmap or ADRs into generated projects.

### Changed

### Fixed

## [0.1.0] - 2026-11-07

First stable release. It is a versioned collection of configurations, engineering
rules, documentation and one small project overlay, composed from maintained
tools instead of a development framework.

Scope, deliverables and limitations are in the
[v0.1.0 release notes](docs/releases/v0.1.0.md); the evidence behind every
acceptance claim is in the
[v0.1.0 acceptance report](docs/releases/v0.1.0-acceptance-report.md). Linux
x86-64 is the only verified platform, and nothing is published to a package
index: ai-devkit is a Git template source, not a Python distribution.

### Added

- A reproducible toolchain. `mise.toml` and `mise.lock` pin Python 3.13.18,
  Node.js 24.22.2, uv 0.13.7, OpenSpec 1.16.0, OpenCode 1.19.5 and the OpenAI
  Codex CLI 0.163.0 with checksums and download URLs, and `.mise/locks/` records
  the npm sidecar lock for OpenSpec. `pyproject.toml` and `uv.lock` pin the
  maintainer's Python environment.
- Python script project initialization. Native `uv init` creates the application,
  then the Copier overlay in `templates/python-script-overlay/template/` adds
  engineering rules, mise tasks, Ruff/mypy/pytest policy, Diátaxis documentation
  seeds and ignore rules. The overlay never renders `main.py`,
  `pyproject.toml`, `uv.lock` or `.python-version`.
- Shared engineering rules in `AGENTS.md`: a reuse-first workflow, quality gates,
  security rules and a Definition of Done, portable across harnesses.
- Native OpenSpec specification and change workflow. `openspec` is initialized by
  its own CLI, `openspec/specs/` and `openspec/changes/` are the only requirement
  and task record, and validation is the native
  `openspec validate --all --strict --no-interactive`.
- OpenCode and Codex integration. OpenSpec generates `.opencode/` and `.agents/`
  for the pinned CLIs, and credential-free configuration examples for OpenCode
  with DeepSeek, the Codex CLI with ChatGPT authentication and optional Cline ship
  under `examples/agents/`.
- Diátaxis documentation built with Zensical in strict mode, so a broken internal
  link fails the build.
- Repository verification with `mise run check` (locked dependencies, agent
  examples, specifications, strict documentation) and a generated-project
  integration test with `mise run test-template`.
- A read-only GitHub Actions workflow that installs the locked toolchain, runs the
  same mise tasks and fails if verification changed a tracked file. It holds
  `contents: read`, no secret and no model call.
- A Copier overlay update lifecycle. Native `copier update` advances
  `.copier-answers.yml`, preserves project-owned code, manifests, tests and
  documentation, and reports an independent edit to the same region of an
  overlay-owned file as a visible, resolvable conflict instead of a silent
  overwrite.
- A `CHANGELOG.md` and a mandatory changelog policy in `AGENTS.md`, so that
  user-visible changes are recorded once, under `[Unreleased]`, until a release
  moves them into a version section.
- Projects generated from the overlay inherit the same discipline: the template
  renders a `CHANGELOG.md` with an empty `[Unreleased]` section and the changelog
  rule in its own `AGENTS.md`. After generation the project developer owns its
  release history, and a `copier update` preserves entries the project has added.
- An MIT licence.

### Changed

- Release documentation names the tag `v0.1.0` as the recommended Copier
  reference. `--vcs-ref HEAD` stays documented as a development-only alternative,
  because a dirty working tree records a synthetic commit and a later
  `copier update` fails with `ValueError: Unknown revision`.

### Fixed

- Documented OpenCode invocations now match the pinned CLI. A one-shot run is
  `opencode run --model <provider>/<model> "<message>"`, not a bare
  `opencode -m …` (which starts the interactive interface and needs a terminal);
  `opencode auth login` accepts an optional `--provider` shortcut, while its
  positional argument is a URL and rejects a bare provider id.

### Known limitations

- Linux x86-64 only; `mise.lock` declares `lockfile_platforms = ["linux-x64"]`.
  macOS, Windows and WSL2 are not verified and are not claimed.
- The generated project is an unpackaged application: no build backend, nothing
  published, no containers, no extra profiles and no orchestration.
- OpenSpec validation passes vacuously while `openspec/specs/` is empty; the first
  specification is what the check actually verifies.
- Whether a harness injects `AGENTS.md` automatically is not established. The
  recorded live sessions read it when asked to, which is a weaker claim.

[Unreleased]: https://github.com/Semtexcz/ai-devkit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Semtexcz/ai-devkit/releases/tag/v0.1.0
