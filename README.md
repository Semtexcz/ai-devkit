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

## Vision and roadmap

The target is autonomous software delivery, not merely more productive manual
coding: a person states a requirement, answers the questions that genuinely need
a human, authorizes what carries real consequence, and accepts delivered software.

- [docs/vision.md](docs/vision.md) — mission, the target autonomous lifecycle,
  human approval boundaries, ownership boundaries, non-goals and how success is
  measured.
- [docs/plans/roadmap.md](docs/plans/roadmap.md) — the implemented v0.1 baseline
  and the provisional milestones after it. Every milestone after v0.1 is a
  proposal, not approved scope.
- [docs/explanation/lessons-from-ai-project-template.md](docs/explanation/lessons-from-ai-project-template.md)
  — what is retained, adapted, delegated, deferred or rejected from the earlier
  `_ai_project_template`.

## Status

Implemented and verified on Linux x86-64 (Tasks 1–6 of the
[historical v0.1 implementation plan](docs/plans/ai-devkit-v0.1.md)):

- an engineering contract in `AGENTS.md` and two architecture decision records;
- a pinned toolchain: mise installs Python 3.13.18, Node.js 24.22.2, uv 0.13.7,
  OpenSpec 1.16.0, OpenCode 1.19.5 and the OpenAI Codex CLI 0.163.0 from
  `mise.lock`, with npm sidecar locks under `.mise/locks/`;
- a locked Python development environment (Copier, pytest, Ruff, mypy, Zensical)
  managed by uv in `pyproject.toml` and `uv.lock`;
- credential-free native configuration examples and setup documentation for
  OpenCode with DeepSeek, the Codex CLI with ChatGPT authentication, and optional
  Cline — documented, validated against the pinned CLIs, and replaceable;
- a Copier overlay that turns native `uv init` output into a verified Python script
  project: engineering rules, mise tasks, Ruff/mypy/pytest configuration, Diátaxis
  documentation and ignore rules. It never renders application code,
  `pyproject.toml`, `uv.lock` or `.python-version`;
- OpenSpec initialized natively with `openspec init --tools opencode,codex --profile
  core`: `openspec/specs/` holds real behavioral specifications, and OpenSpec's own
  OpenCode and Codex integrations live in `.opencode/` and `.agents/`;
- `mise run check` includes the native `openspec validate --all --strict
  --no-interactive`, and a generated project's check runs the same command;
- a generation integration test (`mise run test-template`) that creates a project
  with spaces in its path, installs the exact baseline dependencies, initializes
  OpenSpec with the project's own pinned CLI, runs the application and its smoke
  test, proves each of the six failure modes the contract names fails the check for
  its own reason, and executes one complete change lifecycle from
  `examples/openspec-change/`;
- native `copier update` lifecycle tests between two temporary tagged overlay
  revisions: an edited application, a project regression test, `pyproject.toml`,
  `uv.lock` and project documentation survive; a same-region edit to `AGENTS.md`
  stays visible, resolvable and reviewable; `.copier-answers.yml` advances without
  rewriting anything else;
- a read-only GitHub Actions workflow that installs the locked toolchain and runs
  the same mise tasks, then fails if verification changed a tracked file;
- a Zensical documentation site with strict internal-link validation, exposed as
  `mise run docs`, `mise run docs-serve` and `mise run check`.

Task 7 replays the documented installation and project-creation journey on a
disposable Ubuntu 24.04.5 x86-64 machine and records the evidence in the
[v0.1.0 acceptance report](docs/releases/v0.1.0-acceptance-report.md). Hosted CI has run
green on the reviewed commits. Live agent acceptance was supplied by the user, who ran
one bounded task with OpenCode + DeepSeek Flash and one review with Codex + ChatGPT in a
generated project; the report records those sessions as *user-provided* and states what
they do and do not establish.

v0.1.0 is the first stable release. Its notes are in
[docs/releases/v0.1.0.md](docs/releases/v0.1.0.md), and the changes are listed once, in
[CHANGELOG.md](CHANGELOG.md). **The `v0.1.0` tag is created by a human**, following the
[publication procedure](docs/releases/v0.1.0.md#publish-the-release-tag); no automated
change creates, moves or pushes a release tag.

Agent configuration is native to each harness, so no model or provider is a
dependency of the devkit, and no check makes a paid model request.

## Quick start

Prerequisites: Linux x86-64, Git, `curl`, `tar`, CA certificates, and no need
for `sudo`.

```bash
mise trust                       # after reviewing mise.toml
mise install --locked            # runtimes and CLIs from mise.lock
mise exec -- uv sync --locked    # Python tools from uv.lock
mise run check                   # locked deps, agent examples, specs, strict docs
```

mise itself is installed manually; see
[docs/tutorials/getting-started.md](docs/tutorials/getting-started.md) for the
step-by-step version, including checksum verification.

## Create a project

The overlay is a Copier template. Render it from the release tag:

```bash
mise exec -- uv run --locked copier copy --vcs-ref v0.1.0 --defaults \
  gh:Semtexcz/ai-devkit "$HOME/projects/my script"
```

`--vcs-ref v0.1.0` is the stable reference for a project that should later receive
overlay updates. `--vcs-ref HEAD` renders the current checkout instead and stays
documented as a development-only alternative: on a dirty tree it records a synthetic
commit that a later `copier update` cannot resolve.

An existing project applies a newer overlay with `copier update --vcs-ref <tag>
"<path>"`; the procedure and the conflict review are in
[docs/how-to/update-project-overlay.md](docs/how-to/update-project-overlay.md), and the
end-to-end walkthrough is
[docs/tutorials/first-python-project.md](docs/tutorials/first-python-project.md).

## Toolchain ownership

| Concern | Owner | Lockfile |
|---|---|---|
| Runtimes and CLI versions | mise | `mise.lock` (+ `.mise/locks/`) |
| Python environment and dependencies | uv | `uv.lock` |
| Project overlay and its lineage | Copier | `.copier-answers.yml` in each project |
| Behavioral specifications and change tasks | OpenSpec | `openspec/` in each project |
| Documentation structure | Diátaxis | `docs/` |
| Documentation build | Zensical | `zensical.toml` |
| Tasks | mise | `[tasks]` in `mise.toml` |

## Intended v0.1 architecture and stack

| Concern | Tool | Status |
|---|---|---|
| Tool versions, tasks | mise | implemented |
| Python envs, dependencies, lockfiles | uv | implemented |
| Documentation | Diátaxis, Zensical | implemented |
| Python quality | Ruff, mypy, pytest | pinned; run in generated projects |
| Initial scaffold | native `uv init` | implemented (Task 4) |
| Standards/docs overlay | Copier | implemented (Task 4) |
| Specs and change checklists | OpenSpec | implemented (Task 5) |
| Routine coding | OpenCode + DeepSeek | configured, example only |
| Advanced coding | Codex CLI + ChatGPT auth | configured, profile example |
| Optional agent | Cline + DeepSeek | documented, interface-driven |
| Agent configuration | each harness, natively | documented, not automated |
| Agent instructions | AGENTS.md | implemented |
| CI | GitHub Actions | implemented; hosted run green on `685f041` |

## Initial focus

The only v0.1 profile is an **unpackaged Python application or script**: a
runnable entry point, one smoke test, linting, type checking and documentation.
Packaging, publishing, containers, extra profiles and orchestration are deferred.

## Independence from `_ai_project_template`

`ai-devkit` is independent of `_ai_project_template`: it keeps that project's
emphasis on small slices, executable checks and explicit ownership, but replaces
its policy resolver, context router and lifecycle with native configuration. No
code is shared. The
[lessons page](docs/explanation/lessons-from-ai-project-template.md) records, per
capability, what was retained, adapted, delegated, deferred or rejected.

## Documentation

The documentation site uses Diátaxis and is built with Zensical
(`mise run docs`, preview with `mise run docs-serve`). Entry point:
[docs/index.md](docs/index.md).

- [Getting started](docs/tutorials/getting-started.md) — install the toolchain and build the docs.
- [Create your first Python project](docs/tutorials/first-python-project.md) — `uv init`, the Copier overlay and native OpenSpec initialization, verified end to end.
- [Plan, implement and archive one change](docs/tutorials/spec-driven-change.md) — the complete OpenSpec lifecycle on a real `--name` argument.
- [Install the development toolchain](docs/how-to/install-toolchain.md) — install, update, roll back.
- [Initialize OpenSpec in a project](docs/how-to/initialize-openspec.md) — native init, another agent integration, generated-file updates.
- [Validate changes and specifications](docs/how-to/validate-openspec.md) — the native command and the common validation failures.
- [Update a project's overlay](docs/how-to/update-project-overlay.md) — the native Copier update procedure and conflict resolution.
- [Diagnose a failed CI job](docs/how-to/diagnose-ci-failure.md) — reproduce it locally and read the failure.
- [Configure coding agents](docs/how-to/configure-coding-agents.md) — OpenCode with DeepSeek, Codex with ChatGPT, optional Cline.
- [Troubleshoot agent setup](docs/how-to/troubleshoot-agent-setup.md) — missing credentials, rejected model identifiers.
- [Tool ownership and pinned versions](docs/reference/tool-versions.md) — the tested version tuple.
- [Generated project: commands and contents](docs/reference/generated-project.md) — what the overlay renders, what it runs and what it proves.
- [Continuous integration](docs/reference/continuous-integration.md) — triggers, permissions, pinned actions, limitations.
- [OpenSpec: commands, generated files and validation](docs/reference/openspec.md) — paths, owners, workflows and harness syntax.
- [Agent configuration](docs/reference/agent-configuration.md) — locations, precedence, credentials, verified capabilities.
- [Reproducibility and Python ownership](docs/explanation/reproducibility.md) — why mise and uv are separate.
- [Who owns which file in a generated project](docs/explanation/generated-project-ownership.md) — uv versus Copier versus mise versus OpenSpec.
- [Why verification and updates share one command](docs/explanation/verification-and-updates.md) — one definition of correct, reviewed updates, independent files.
- [OpenSpec, AGENTS.md and ADRs](docs/explanation/openspec-and-agents.md) — requirements, tasks, standards and rationale.
- [Why agent configuration stays native](docs/explanation/agent-independence.md) — no router, separate billing paths.
- [Product vision](docs/vision.md) — mission, target autonomous lifecycle, human approval boundaries, non-goals and success measures.
- [Roadmap](docs/plans/roadmap.md) — the implemented v0.1 baseline and the provisional milestones after it; milestones after v0.1 are not approved scope.
- [Lessons from `_ai_project_template`](docs/explanation/lessons-from-ai-project-template.md) — what was retained, adapted, delegated, deferred and rejected.
- [ADR 0001](docs/explanation/decisions/0001-minimal-devkit.md) — design rationale.
- [ADR 0002](docs/explanation/decisions/0002-script-project-overlay.md) — overlay scope and provenance.
- [Historical ai-devkit v0.1 implementation plan](docs/plans/ai-devkit-v0.1.md) — the implementation record for the implemented baseline; its backlog is spent.
- [v0.1.0 release notes](docs/releases/v0.1.0.md) — what v0.1 delivers, what it does not, and how the release tag is published.
- [v0.1.0 acceptance report](docs/releases/v0.1.0-acceptance-report.md) — per-scenario evidence, environments and the user-provided live sessions.
- [CHANGELOG.md](CHANGELOG.md) — notable changes, in Keep a Changelog form.
- [LICENSE](LICENSE) — MIT.
- [AGENTS.md](AGENTS.md) — engineering rules for agents and humans, including the changelog policy.

## Licence

ai-devkit is released under the [MIT licence](LICENSE).

Generating a project from this template does not decide that project's licence. The
overlay renders engineering policy, not legal terms, so a generated project starts
without a licence file and choosing one is the project developer's decision.
