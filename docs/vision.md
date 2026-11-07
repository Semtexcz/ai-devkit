# Product vision

`ai-devkit` is a portable, versioned integration platform for progressively
autonomous software development.

The strategic target is **autonomous software delivery**: a person states a
requirement, answers the questions that genuinely need a human, authorizes the
actions that carry real consequence, and receives accepted software. More code
per hour of manual agent operation is a side effect, not the goal.

This page states the durable direction. It is not an implementation plan.
[The roadmap](plans/roadmap.md) records what exists today and what each future
milestone would add, and only an approved OpenSpec change authorizes
implementation.

## Mission

Minimize the human attention one accepted software delivery requires, subject to
quality, safety and sustainable cost.

All three constraints bind. The delivered software must be correct and
verifiable; the platform must not take irreversible or consequential actions
without human authorization; and cost must be predictable, not merely small.

## What the human becomes

The human acts primarily as a customer and Product Owner, not as a continuous
programmer or agent operator. That means:

- stating requirements and answering the questions that only the product owner
  can answer;
- approving significant actions: scope, releases, spending beyond a budget,
  credentials, deployments and anything irreversible;
- reviewing demonstrations rather than reading every diff;
- accepting or rejecting delivered software.

The human does not become a queue operator. A platform that needs a human to
start each step has not delivered this vision, however productive each step is.

## The autonomous development lifecycle

The target lifecycle moves a requirement to accepted software with a bounded
number of human touchpoints:

| Stage | Target behavior | Human involvement |
|---|---|---|
| Requirement capture | The requirement enters the product repository and becomes an approved specification and change task list | States the requirement; approves the specification |
| Clarification | Ambiguities that change behavior are collected and asked as one batch | Answers; the answer becomes durable context |
| Planning | The work is decomposed into an ordered, dependency-aware set of changes | Approves significant scope changes only |
| Implementation | An agent implements the smallest coherent change against the approved specification | None |
| Verification | Existing deterministic checks (lint, types, tests, docs build, specification validation) produce the evidence | None |
| Independent review | A second pass judges the actual diff, not the implementer's summary | None, until a review blocks |
| Repair | Failed checks or review findings are retried within an explicit bound, then escalated | Only when the bound is exhausted |
| Delivery | The change is integrated and released or handed over with its evidence | Approves publication where the project requires it |
| Acceptance | The delivered software is demonstrated against the accepted specification | Accepts or rejects |

The lifecycle is the unit of design. Each stage has one authoritative owner, and
no stage may silently take over another stage's decision.

## Target capabilities

These are strategic requirements. **None of them is a v0.1 capability**, and each
names the milestone that would make it real; see the [roadmap](plans/roadmap.md).

- Long-running autonomous development cycles.
- Durable state and automatic recovery after interruptions and restarts.
- Agent orchestration with bounded retries and repair loops.
- Cost-aware selection of agents and models.
- Two-way communication through Telegram or an equivalent interface.
- Human-in-the-loop clarifications and approvals.
- A dashboard showing progress, blockers, verification evidence and costs.
- Optional unattended execution locally or on a VPS.
- Parallel agents using isolated Git worktrees where appropriate.
- Independent review before a change is considered ready.
- Final human product acceptance.

Responsibility for those capabilities does not belong to `ai-devkit`:

| Capability | Owner |
|---|---|
| Behavioral specifications and change tasks | OpenSpec |
| Execution, provider access, sessions, credentials | Native agent harnesses |
| Scheduling, task execution state, retries, pending questions, approvals, recovery | A future orchestrator, selected only when that milestone is approved |
| Deterministic technical evidence | Existing verification tools and CI |
| Product decisions, consequential authorizations, final acceptance | The human |

**The orchestrator is not selected.** When that milestone is approved, existing
maintained solutions are evaluated on evidence: durable state, restart recovery,
bounded retries, human approval gates, a messaging surface, harness and model
neutrality, licensing and maintenance. Cezar and Vibe Kanban are candidates, not
commitments, and naming one here makes nothing a dependency.

The existing foundation must stay useful without an orchestrator: every v0.1
capability works with no coordinating process, and no milestone may make a
coordinator mandatory for ordinary project work.

## Long-running execution and its surface

The target platform is not a chat session that a person keeps alive. It runs
development cycles of hours or days, so its own operation has to survive a closed
terminal, a reboot or a dropped network connection.

| Concern | Target |
|---|---|
| Duration | Multi-hour and then multi-day cycles, with no human present for the duration |
| Continuity | Durable state that survives interruption, restart and recovery; nothing important lives only in a conversation |
| Conversation | Two-way Telegram (or an equivalent) messaging: questions arrive where the human already is, and the answer returns as durable context |
| Oversight | A dashboard for progress, blockers, verification evidence and spend, plus a batched question inbox instead of drip-fed interruptions |
| Place | Unattended execution locally, or on an optional VPS when a machine must stay up |
| Bounds | Explicit budgets, retry limits and a stop condition, so unattended work cannot spend without limit |

Both the messaging surface and the dashboard are views over the orchestrator's
state, not a second source of truth, and neither may hold a decision the
orchestrator does not record.

## Human approval boundaries

Approval is a human authority. A platform that can manufacture its own approval
has no approval boundary at all.

| Domain | The human decides | Agents may decide |
|---|---|---|
| Product | Requirements, scope, milestone approval, acceptance or rejection of delivered software | Implementation choices inside an approved specification |
| Release | Creating, moving and publishing version tags, and publishing artefacts | Preparing a release for review |
| Consequential actions | Credentials, deployments, infrastructure, spending beyond an explicit budget, destructive Git or filesystem operations | Nothing irreversible |
| Repair | Escalation when a retry budget is exhausted, or when the failure is architectural | Repair attempts inside the stated bound |
| Verification | Whether unverified evidence is acceptable | Nothing: a check that did not run is not a pass |

A future orchestrator executes those decisions; it never substitutes for them.
Approval levels, budgets and bounds are configuration, and the human owns the
configuration.

## Reuse-first architecture

`ai-devkit` follows **Reuse → Configure → Extend → Build**:

1. **Reuse** a maintained tool that already solves the problem.
2. **Configure** it through its native configuration.
3. **Extend** it only where the maintained behavior stops.
4. **Build** only project-specific policy.

Custom code is the last resort, and the maintained surface stays small. The
platform owns the integration, the standards, the templates, their compatibility
tests and their documentation; it does not own the work those tools do.

| Concern | Authoritative owner |
|---|---|
| Versioned integration, engineering standards, templates, compatibility tests, documentation | `ai-devkit` |
| A product's requirements, application code, tests, documentation and releases | That product repository |
| Approved behavioral specifications and change tasks | OpenSpec |
| Execution, provider access, sessions and credentials | Native agent harnesses and their own credential stores |
| Deterministic verification | The project's existing checkers and CI |
| Scheduling, retries, waiting questions, approvals and recovery | The future orchestrator, if one is adopted |
| Product decisions and final acceptance | The human |

Duplicating an authoritative owner is a defect, not a convenience.

## Portability and versioning

- **Portable.** No hard dependency on one coding agent, model, provider or
  account. Harness, provider, model, execution profile, role and orchestrator
  stay separate concepts, and each harness keeps its native configuration and
  credential store.
- **Versioned.** Pinned tool versions, locked dependencies, semantic version
  tags and Copier provenance make the foundation reproducible and updatable, so a
  project can state which revision generated it.
- **Reversible defaults.** Defaults are configuration, not requirements; a shared
  standard must outlive the account or the release that made it convenient.
- **Evidence-bound.** No verified claim without a check that ran, and no support
  claim for a platform that was never tested.

## Non-goals

`ai-devkit` will not become:

- a coding agent, a harness fork or a universal agent framework;
- a custom LLM gateway, model router or credential manager;
- a custom task-management system, workflow state machine or policy resolver;
- a hosted service, a deployment platform or an infrastructure provider;
- a replacement for a product repository's requirements, code, tests and
  releases, or for OpenSpec's change record;
- a hard dependency on any single vendor, model, provider or account.

A future orchestrator is evaluated and configured, not written here.

## How success is measured

The primary objective is human attention per accepted delivery. It is measured,
not asserted, and each milestone names the point at which its measurement
becomes possible.

| Dimension | Metric | First measurable at |
|---|---|---|
| Attention | Human interactions and active human minutes between an approved specification and an accepted delivery | M2 |
| Autonomy | Share of deliveries completed with no human code edit; longest unattended run recovered without intervention | M2 (share), M4 (unattended duration) |
| Quality | Share of deliveries accepted at first review; escaped defects found after acceptance | M2 |
| Safety | Consequential actions taken without recorded human authorization, with a target of zero; an approval-boundary violation is a defect | M2 |
| Cost | Cost per accepted delivery, and the share of routine work routed to economical models, taken from harness-reported usage | M2 |
| Recovery | Share of interruptions recovered without human intervention, and time to resume | M2 (single change), M4 (unattended) |
| Reproducibility | Whether a milestone is reproducible from its pinned versions on a documented platform | M0 |

No number in this vision is a current measurement. Until a milestone produces
evidence, the honest statement is that the metric is unmeasured.

## Where this vision stands today

v0.1.0 delivers the foundation the vision builds on: pinned tools, engineering
rules, one project overlay, OpenSpec as the requirement and change record,
deterministic verification locally and in CI, and documentation. It does not
deliver autonomy, orchestration, messaging, a dashboard, durable run state or
unattended execution. The [roadmap](plans/roadmap.md) records the baseline and
the gaps honestly, and
[Lessons from `_ai_project_template`](explanation/lessons-from-ai-project-template.md)
records which earlier experiments were kept, adapted or deliberately not
repeated.
