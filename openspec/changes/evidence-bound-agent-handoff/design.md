# Design

## Context

See `proposal.md` for motivation. The project already has one authoritative owner
for each fact this procedure needs: OpenSpec for the approved change and its task
list, Git for commits and diffs, the project's checks and CI for automated
verification, native harnesses for sessions, and the human for approval. The
[product vision](../../../docs/vision.md) already records those ownership and
approval boundaries.

The gap is procedural: the pilot's handoff had no written minimum, so a reviewer
had to infer what was in scope and a human could not tell a verified result from an
agent's summary.

## Goals / Non-Goals

**Goals:**

- Make one handoff record sufficient for an independent reviewer to start without
  the implementer's session state.
- Make the repair loop bounded and auditable against the original findings.
- Make the final record state exactly what a human is approving.
- Keep the procedure usable by any harness and by humans without an orchestrator.

**Non-Goals:**

- An executable workflow engine, state machine, task database or agent router.
- Automating role selection, model choice, retries, merges or releases.
- Replacing OpenSpec, Git, CI or a harness's own session record.
- Defining model-specific prompts or providers.

## Decisions

- **One how-to plus OpenSpec requirements, not a schema.** The procedure is prose
  and checklists because a machine-readable state file would duplicate owners that
  already hold the facts. `openspec validate` makes the behavioral promises
  checkable; the how-to explains how a person or agent produces them.
- **Four handoffs, one evidence vocabulary.** Implementation → review → repair →
  review → human. Each stage consumes the previous record instead of re-deriving
  context, which is what keeps the reviewer independent and the repair bounded.
- **Provenance is explicit.** Every claim is `verified`, `self-reported` or
  `unavailable`. A verified claim names the commit, command output or CI run that
  establishes it. This is the core defense against a polished summary substituting
  for evidence, and it is what makes the Bookvoice pilot record honest.
- **A fixed verdict vocabulary.** Review ends with `APPROVE` or
  `REQUEST CHANGES`; blocking findings are separated from observations. The repair
  bound is two unsuccessful attempts, matching the policy already recorded in the
  roadmap and vision, after which the work escalates to a human.
- **Approval attaches to a commit.** A repair creates a new head, so the final
  handoff must cite the review and CI result for that exact commit. Approving a
  branch generally would let an unreviewed commit travel with an old approval.
- **Ownership stays where the vision put it.** The how-to links to the vision
  rather than restating the approval table. A future orchestrator may coordinate
  the stages, but it must read and write these same sources and must not become a
  second source of truth.

## Risks / Trade-offs

- [The handoff becomes heavy enough that agents skip it] → Keep one record with a
  short field list; require detail only where a reviewer or human would otherwise
  have to guess.
- [A reviewer rubber-stamps the implementer's summary] → Require a diff-first review,
  reproducible findings and an explicit verdict; make the pilot's self-report
  boundary an example.
- [A repair widens scope] → Require the exact findings, a regression test per
  confirmed defect and a stop after two unsuccessful attempts.
- [The documentation drifts from practice] → Validate the requirements with
  OpenSpec and cite one real pilot; add another pilot before claiming the procedure
  is proven across projects.
- [The procedure is mistaken for autonomous delivery] → State in the how-to and the
  pilot record that a human coordinates every stage and performs the merge.

## Migration Plan

No migration. The how-to is additive documentation; existing projects and
workflows are unaffected until they choose to follow it.

## Open Questions

None that change the requirements or task breakdown.
