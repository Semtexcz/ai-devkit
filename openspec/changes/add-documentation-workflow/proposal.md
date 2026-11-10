# Proposal

## Why

ai-devkit already builds documentation strictly and defines independent review,
but has no reusable contract for deciding which documentation needs an update,
writing it from evidence, or auditing its accuracy. A small manual workflow can
close that gap across README-only and larger repositories without adopting an
orchestrator or another documentation framework.

## What Changes

- Propose one shared documentation standard, a Documentation Writer skill and a
  separate, read-only Documentation Auditor skill. Both consume the same standard
  and project rules; external writing or classification guidance remains optional.
- Define evidence-based impact assessment, minimal edits, independent findings,
  P0–P3 severities, explicit incomplete outcomes and bounded remediation using the
  existing review-and-repair handoff.
- Deliver an opt-in, manual MVP as documentation and inert skill examples. No
  repository-wide rewrite, mandatory documentation tree or site generator.
- Evaluate all six requested upstream skills in [research.md](research.md),
  including dependencies, observed licenses, maintenance signals and conflicts.
  Prefer selected reuse over installing whole collections or copying their tools.
- Describe later agent coordination and deterministic CI adoption in
  [design.md](design.md), without authorizing either implementation. Cezar remains
  an unselected candidate and owns orchestration state only if separately adopted.

### Goals

Make documentation changes necessary, accurate, concise and reviewable; detect
consequential drift with evidence; preserve useful existing material; support
incremental adoption without a specific agent, model or provider.

### Non-goals

This request creates planning artifacts only. It does not implement or install
skills, change production code or the overlay, create a pull request, select an
orchestrator, change Cezar's engine, add dependencies, or authorize a milestone.
The proposed MVP excludes automatic skill synchronization, export pipelines,
LLM-based CI, an audit database and a custom workflow/state schema.

## Capabilities

### New Capabilities

- `documentation-standard`: A proportional, evidence-based standard and explicit
  ownership and external-component boundaries shared by both roles.
- `documentation-authoring`: Repository inspection, documentation impact decisions
  and minimal, verified writing across supported documentation genres.
- `documentation-auditing`: Independent, immutable audits with actionable findings,
  explicit progression gates and bounded manual remediation.

### Modified Capabilities

None. The MVP consumes `evidence-bound-agent-handoff` and
`devkit-ci-verification` without weakening or replacing their requirements.

## Impact

After separate implementation approval, add a standard under `docs/reference/`, a
manual procedure under `docs/how-to/`, and two inert examples under
`examples/skills/`. Add navigation, a short discovery link in engineering rules,
an ADR for skill ownership and the implementation changelog entry. Existing
project documentation remains project-owned; no `.agents/`, `.opencode/`,
`openspec/config.yaml`, Copier source, lockfile or CI runtime change is proposed
for the MVP. No new runtime dependency is required.

The current proposal changes only its OpenSpec change directory. Its acceptance
matrix, risks, unresolved human decisions and deferred integration conditions are
in the design; implementation tasks remain unchecked.
