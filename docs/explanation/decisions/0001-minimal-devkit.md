# 0001 — Minimal configuration-first devkit

- **Status:** Accepted
- **Date:** 2026-11-05

## Context

`ai-devkit` supports small Python projects developed with coding agents. The
known alternative, `_ai_project_template`, reaches this with a custom policy
resolver, context router, task-state store and release tooling to maintain and
audit indefinitely, while recreating what existing tools already provide. The
goal is low-maintenance delivery on a small, reviewable surface.

## Decision

`ai-devkit` is a versioned collection of configurations, standards, documentation
and a minimal project overlay, not a development framework.

1. It ships as that collection, not as an application or CLI.
2. mise owns runtime and tool versions, their lockfiles and development task
   definitions.
3. uv owns Python environments, project dependencies and dependency lockfiles.
4. Python selection must be consistent: implementation must verify uv uses the
   version mise selects.
5. Native `uv init` creates the initial Python scaffold; the devkit keeps no
   template for it.
6. Copier provides the standards/documentation overlay and tracks its lineage,
   never owning application code, `pyproject.toml` or `uv.lock`.
7. OpenSpec is the intended single source of truth for specifications and change
   checklists.
8. Harness, provider, model, execution profile, role and orchestrator are separate
   concepts with separate owners; no shared role-to-model schema exists.
9. Native agent configuration initially selects models and execution profiles.
10. Automatic role-based routing is deferred, not abandoned; future orchestration
    should use an established tool.
11. Diátaxis and Zensical serve the devkit's documentation; generated script
    projects may use README-based docs, a site being optional.
12. A few native tool commands are preferred over a custom devkit CLI.
13. The devkit must support future compatible agents and providers without
    restructuring shared engineering standards.

These are decisions about ownership, not a claim about implementation status;
the [toolchain reference](../../reference/tool-versions.md) records what is
implemented and verified today.

## Consequences

- Each concern has one owner, so duplication and drift are visible in review.
- The maintained surface stays small: short rules, records and a thin overlay.
- Upstream upgrades arrive free, but upstream breaking changes become this
  project's responsibility.
- Setup uses native commands, so instructions must stay precise and the pinned
  tool tuple is re-tested per release.
- Orchestration stays manual in v0.1.

## Alternatives considered

- **A custom devkit CLI or framework.** Rejected: production code, tests and
  security surface for behavior native commands already provide.
- **Forking an existing Python template.** Rejected for the first profile:
  inspected templates add packaging, publishing or command layers a script does
  not need.
- **A shared role-to-model routing schema.** Rejected: duplicates native agent
  configuration and couples standards to harnesses.
- **Adopting an orchestration engine now.** Deferred: candidates document
  experimental harness support and permissive permissions needing tests.
