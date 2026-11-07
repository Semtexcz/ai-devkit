# Roadmap

This page reconciles the historical `v0.1` plan with the delivered v0.1.0
baseline, and records the provisional milestones that follow it. The strategic
target it serves is the [product vision](../vision.md).

Read it as direction, not as approved scope:

- M0 is delivered; only the claims recorded in the
  [v0.1.0 acceptance report](../releases/v0.1.0-acceptance-report.md) are
  verified.
- **Every milestone after M0 is a provisional proposal.** Naming a capability
  here does not authorize building it.
- Actionable work is owned by OpenSpec. An approved change in `openspec/changes/`
  is the only authorization to implement anything, in any milestone.
- Choosing whether to start a milestone is a human decision.

## How to read a milestone

Each milestone states the same five things:

- **Outcome** — what a customer can observe that they cannot observe today.
- **Baseline** — what already exists and is verified.
- **Gaps** — what is genuinely missing, stated without optimism.
- **Dependencies** — what has to be decided, verified or adopted first.
- **Acceptance** — the evidence that would close the milestone.

Acceptance criteria are gates, not promises. A milestone closes when its
evidence exists, not when its narrative reads well.

## Reconciliation: the historical plan and the delivered v0.1

The `v0.1` plan ([historical implementation plan](ai-devkit-v0.1.md)) carried a
dependency-ordered backlog of seven tasks. That backlog was the only roadmap this
project had, and it is now spent:

| Historical task | State | Where it lives now |
|---|---|---|
| Task 1 — repository contract | delivered | `AGENTS.md`, `README.md`, `.gitignore`, ADR 0001 |
| Task 2 — pinned toolchain and documentation verification | delivered | `mise.toml`, `mise.lock`, `.mise/locks/`, `pyproject.toml`, `uv.lock`, `mise run docs` |
| Task 3 — native agent profiles | delivered as documentation and inert examples | `examples/agents/`, [agent configuration](../reference/agent-configuration.md) |
| Task 4 — Python script overlay | delivered | `copier.yml`, `templates/python-script-overlay/template/`, `mise run test-template` |
| Task 5 — OpenSpec vertical slice | delivered | `openspec/`, [OpenSpec reference](../reference/openspec.md) |
| Task 6 — CI and update behavior | delivered | `.github/workflows/verify.yml`, `tests/`, [continuous integration](../reference/continuous-integration.md) |
| Task 7 — clean-machine journey | delivered and recorded | [v0.1.0 acceptance report](../releases/v0.1.0-acceptance-report.md) |

The plan also listed deferred work. None of it disappeared; it moved to a
milestone or was deliberately dropped as a design choice:

| Historical deferral | Resolution |
|---|---|
| Automatic model escalation, custom cost accounting | M2, and only as orchestration configuration driven by harness-reported usage |
| Orchestration, dashboards, bots and remote services | M2 and M4, delegated to an evaluated orchestrator rather than built here |
| Additional profiles (library, CLI, backend, frontend, fullstack) | Parallel profile track; never a prerequisite for autonomy |
| Package publishing and containers | Not on this roadmap; they are a generated project's decision, not the devkit's |
| Native Windows, macOS and WSL2 support | Deferred until a milestone verifies them; Linux x86-64 remains the only verified platform |
| Extra skill packages and agent installation automation | M1, evaluated against OpenSpec's own generated skills first |

## M0 — Release v0.1.0: a tested, reproducible development foundation

**Outcome.** A person can install a pinned toolchain on Linux x86-64, generate a
Python script project from a tagged overlay, give an agent native
configuration, run one OpenSpec change end to end, and pass the same checks
locally and in CI.

**Baseline.** Implemented; see [v0.1.0 release notes](../releases/v0.1.0.md) and
the [acceptance report](../releases/v0.1.0-acceptance-report.md).

**Gaps.** The release tag itself is a human action and does not exist yet. Linux
x86-64 is the only verified platform. One profile exists. There is no
orchestration, durable run state, messaging, dashboard or cost accounting, and
none is claimed.

**Dependencies.** Human review of the acceptance report, a green hosted CI run on
the tagged commit, and the human [tag publication](../releases/v0.1.0.md#publish-the-release-tag).

**Acceptance.**
`mise run check` and `mise run test-template` pass on the tagged revision; a
throwaway project renders from the tag, records `_commit: v0.1.0` and reports
`Project is up-to-date!`; `CHANGELOG.md` describes the tagged version.

## M1 — Engineering maturity

**Outcome.** Ordinary project work becomes cheaper and more reliable per change:
the same standards are reusable across real projects, an agent loads less
irrelevant context, and the checks catch more before a review does.

**Baseline.** v0.1 supplies `AGENTS.md`, one overlay, OpenSpec's generated
skills, the six-check verification contract and a generation and update test. The
`v0.1` plan already recorded a cost policy — implement bounded, stop after two
failed repairs and hand the evidence on — as a documented rule rather than an
engine.

**Gaps.**
- Skills are whatever OpenSpec generates; there are no devkit-owned reusable
  procedures for orienting, implementing, verifying, reviewing or capturing a
  lesson.
- Context loading is a prose instruction ("read only what the task needs"), not a
  measured or routed budget, so cost per change is unmeasured.
- The workflows are documented but only exercised by this repository's own
  tests, not by several real product projects.
- A recurring failure becomes a prompt or a paragraph; the project has no
  explicit rule that prefers an executable check over documentation.

**Dependencies.** At least two real generated projects as evidence; a decision on
whether skills belong to OpenSpec, to the overlay or to the devkit; a
measurement of context cost that does not require an orchestrator.

**Acceptance.** Reusable procedures exist and are validated as files, not copied
by hand; a measured context bundle exists for at least one real change; every
recurring failure discovered during the milestone is recorded as an executable
check where one is possible; a decision record states what was rejected and why.

**Provisional.** No skill library, context router or policy resolver is approved
by this page; the reference lessons in
[Lessons from `_ai_project_template`](../explanation/lessons-from-ai-project-template.md)
show why each was deferred.

## M2 — Recoverable single-change autonomy

**Outcome.** A human writes a requirement, answers one batched set of questions if
needed, and receives one independently reviewed, verified and integrated change.
If the machine is interrupted, the work resumes without losing the task, the
branch or the evidence, and the human can follow progress and spend from a
dashboard or a Telegram conversation.

**Baseline.** One change can already be specified, implemented, verified and
reviewed by humans driving harnesses by hand. The repositories already provide
the boundaries an orchestrator would call: OpenSpec change tasks, `mise run
check`, CI, and the native harnesses.

**Gaps.** No durable run state, no scheduling, no bounded retry loop, no pending
question queue, no messaging surface, no dashboard and no cost aggregation. The
orchestrator is unselected.

**Dependencies.**
- A human decision to start the milestone.
- An evidence-based evaluation of maintained orchestrators, judged on durable
  state, restart recovery, bounded retries, approval gates, a messaging surface,
  harness and model neutrality, licensing and maintenance. Cezar and Vibe Kanban
  are candidates, not commitments; a "build our own" outcome is a failure of the
  evaluation, not a plan.
- A decision on where execution state lives, so that it has one owner and is not
  duplicated in Git, in a harness session and in a dashboard.
- A cost policy fed by harness-reported usage, with no invented price table.

**Acceptance.** For one approved change: bounded implementation and repair with an
escalation when the bound is exhausted; a review performed without the
implementer's session state and reported as findings before a readiness verdict;
one clarification round-trip through the messaging interface, recorded as durable
context; a forced interruption followed by automatic recovery with no lost state;
an approval that only a human could produce; dashboard or messaging status
matching the actual repository and verification state; measured human
interactions and cost per accepted delivery for that change.

**Provisional.** Which orchestrator, if any, and which messaging transport are
open decisions.

## M3 — Parallel autonomous delivery

**Outcome.** Several independent changes progress at the same time without
interfering with each other, and the human answers one consolidated question set
rather than several, then accepts the delivered product as a whole.

**Baseline.** M2 delivers single-change autonomy. Task decomposition already
comes from OpenSpec change tasks, which carry dependencies.

**Gaps.** No worktree isolation, no claim or lease over a task, no dependency-aware
scheduling, no integration ordering, no CI-driven repair loop across branches, no
question consolidation and no product-level acceptance demonstration.

**Dependencies.** M2 closed; a worktree and claim decision (Git native, or the
orchestrator's); a merge policy that keeps the human merge as the approval
boundary; conflict and integration evidence.

**Acceptance.** At least three independent changes delivered concurrently in
separate worktrees with no cross-contamination; dependency order respected;
integration verified by the project's own checks; a failed CI run repaired by a
fresh bounded session on the same branch; at most one consolidated human question
batch per cycle; a demonstration reviewed by the human before acceptance.

**Provisional.** The concurrency limit, the integration strategy and the
question-batching policy are open decisions.

## M4 — Dependable unattended operation

**Outcome.** The platform runs for hours or days with no human present, on a
workstation or an optional VPS, and a human can leave it alone without losing
work, money or safety.

**Baseline.** M3 delivers parallel delivery under supervision.

**Gaps.** No unattended scheduling, no backup and restore of durable state, no
restart recovery across reboots, no budget enforcement, no kill switch, no audit
trail of consequential actions and no alerting.

**Dependencies.** M3 closed; a hosting decision (local, VPS or both); an
operations decision for secrets, backups and upgrades; a safety decision for
budgets, limits and stop conditions.

**Acceptance.** A multi-day unattended run completes and survives at least one
reboot; durable state restores from backup into a working run; budget exhaustion
stops work and raises a human decision rather than continuing; every
consequential action appears in an audit trail with its authorization; the human
receives an alert instead of discovering a stall; the documented operational
procedures are executed, not merely written.

**Provisional.** Everything about hosting, tenancy and operations.

## Parallel track — additional project profiles

Profiles are a separate axis from autonomy. They add a shape of *project*; they do
not add orchestration, and autonomy must never wait on them.

| Profile | Outcome | Status |
|---|---|---|
| Unpackaged Python script | The v0.1 profile: entry point, one smoke test, lint, types, docs | Delivered |
| CLI application | A command surface with argument-parsing tests | Proposed; needs a real project |
| Library | Packaging, import surface, API documentation and a release story | Proposed; needs a real project |
| Backend service | HTTP surface with contract and integration tests | Proposed; needs a real project |
| Frontend | A browser surface with build and end-to-end checks | Proposed; needs a real project |
| Full-stack | Both surfaces plus their contract | Proposed; last, and only with real demand |

Rules for this track:

- A profile is added when a real project needs it, never to complete a matrix.
- Each profile keeps the same verification contract and the same ownership
  boundaries; a new profile adds configuration, not a second workflow.
- Packaging, publishing and containers stay the generated project's decisions.
  The devkit supplies standards, not a release process it then owns.

## Milestone gates

A milestone is not started because the previous one is finished; it is started
because the evidence exists and a human approves the next scope.

| Gate | Evidence required |
|---|---|
| M0 → M1 | The tag exists, hosted CI is green on it, and at least one real project was generated from it |
| M1 → M2 | The context and skill decisions are recorded, and real-project feedback shows the remaining cost is coordination, not engineering |
| M2 → M3 | One change was delivered autonomously, recovered from an interruption, and its approval was human-only |
| M3 → M4 | Parallel delivery produced verifiable integration evidence and no cross-contamination |
| M4 | Unattended operation survived an interruption, a reboot, a restore and a budget stop |

Any milestone may also be closed as *not worth it*, and that is a legitimate
outcome. A cheaper, more reliable manual workflow that never becomes autonomous
is a real alternative to a fragile orchestrator.

## What this page is not

- It is **not a backlog**. Task-level, approved work lives in OpenSpec:
  `openspec new change`, then `openspec validate --strict`, then `openspec
  archive`. Do not create a second task list, milestone schema or task-state file
  next to it.
- It is **not an authorization**. A milestone description is not scope. Starting
  one requires an approved OpenSpec change and a human decision.
- It is **not a commitment to build**. Where a maintained tool can carry a
  capability, adopting and configuring it beats implementing it.

The historical [v0.1 implementation plan](ai-devkit-v0.1.md) is preserved as
implementation documentation for M0; it is not a live plan and its backlog is
spent.
