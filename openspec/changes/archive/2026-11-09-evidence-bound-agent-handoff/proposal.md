# Proposal

## Why

The Bookvoice pilot showed that an implementer, an independent reviewer and a
repair agent can cooperate on one change, but the evidence a reviewer and the
human needed lived only in agent sessions. Nothing in the repository stated which
commits, commands, results and decisions must travel between the stages, so a
handoff could look complete while remaining unverifiable, and a repair could drift
from the approved scope.

Standardizing the minimum evidence now makes the same procedure reusable across
OpenCode, Codex, Cline or another harness, without building an orchestrator.

## What Changes

- Add one harness-agnostic how-to,
  `docs/how-to/review-and-repair-one-change.md`, covering the four handoffs:
  implementation to review, review to repair, repair to review and review to human.
- Define observable requirements for the minimum implementation evidence, the
  independent review, the bounded repair and the final verification and human
  approval, plus the provenance label every claim must carry.
- Record Bookvoice PR #4 as one worked pilot: verified repository and CI facts are
  separated from agent self-reports, and the pilot is explicitly human-coordinated
  rather than autonomous delivery.
- Link the how-to from the documentation index and navigation, and record the
  user-visible addition in `CHANGELOG.md`.

No new dependency, task-state file, workflow schema, agent router, generated-file
change or hard-coded model/provider requirement is introduced.

## Capabilities

### New Capabilities

- `evidence-bound-agent-handoff`: the minimum evidence and verdicts required when
  one change passes from implementation to independent review, bounded repair and
  final human approval

### Modified Capabilities

None.

## Impact

- `docs/how-to/review-and-repair-one-change.md` (new)
- `docs/index.md` and `zensical.toml` (link and navigation)
- `CHANGELOG.md`
- `openspec/changes/evidence-bound-agent-handoff/`
- No application code, dependency, template, CI workflow, generated file or release
  tag changes.
