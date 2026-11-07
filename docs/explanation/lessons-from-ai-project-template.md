# Lessons from `_ai_project_template`

`_ai_project_template` is the earlier project that `ai-devkit` deliberately does
not copy. Its engineering experience is still the most complete evidence this
project has about agent-driven development, so this page records what was worth
keeping, what needed adapting, what should be delegated to a maintained tool,
what is deferred, and what is rejected.

## Scope and evidence

- Reviewed at commit
  [`d035235`](https://github.com/Semtexcz/_ai_project_template/tree/d035235c09cf057665cdc526acffa231724b9614),
  the same revision the [v0.1 plan](../plans/ai-devkit-v0.1.md) audited.
- Evidence is its documentation, its agent layer, its tooling entry points and
  its test names: `docs/`, `AGENTS.md`, `.agents/`, `project/`, `tools/`,
  `template/tools/` and `tests/`.
- **No execution.** Nothing in that repository was installed, rendered or run for
  this review, and no model was called. Claims about its behavior rest on its own
  documentation and tests, which is weaker evidence than a reproduced run. Every
  link below points at that pinned commit, so a later change upstream does not
  silently rewrite this page's evidence.

## Decision vocabulary

| Decision | Meaning |
|---|---|
| **Retain** | The lesson is already right; keep the behavior and its reasoning |
| **Adapt** | Keep the insight, change the implementation to fit the maintained-tool boundary |
| **Delegate** | A maintained external tool should own it; `ai-devkit` configures or adopts that tool |
| **Defer** | Worth doing, but only after a named milestone and its evidence |
| **Reject** | Deliberately not repeated; the reason is a design decision, not an oversight |

## Decision matrix

| Capability | Evidence in `_ai_project_template` | Decision | What `ai-devkit` does |
|---|---|---|---|
| Progressive architecture | A small AI kernel plus independent `project_type`, `runtime_level`, `governance` and `workflow_mode` axes; presets are conveniences only ([template-architecture.md][ref-arch]) | **Adapt** | One profile, added only when a real project needs it; no render matrix, no golden path per combination ([roadmap](../plans/roadmap.md)) |
| Atomic skills | One concern per `.agents/skills/*/SKILL.md` with `purpose`, `triggers`, `reads`, `commands`, `outputs`, `approval_boundary` and `stop_conditions` ([implement-change][ref-implement], [review-change][ref-review]) | **Adapt** | OpenSpec generates the skills that exist, so the devkit ships no second skill library; the frontmatter shape is a candidate for milestone M1 |
| Context efficiency | Tiered loading with a deterministic budget (`max_files`, `max_bytes`), path-to-context routing and never recursing into a directory ([context-map.yaml][ref-context]) | **Defer** the machinery, **retain** the principle | `AGENTS.md` states "load only the context the task needs"; M1 measures context cost on real changes before any routing exists |
| Definition of Done | One shared definition of when work is complete, applied to every task ([AGENTS.md][ref-agents]) | **Retain** | Already in `AGENTS.md` here, including the changelog and verification clauses |
| Executable checks | One validation-only `make check`, explicit mutating commands, and focused checks during implementation ([template-architecture.md][ref-arch]) | **Retain** | `mise run check` is validation-only and must not rewrite tracked files; `mise run docs` fails on a broken link |
| Independent review | A review that inspects the actual diff, reports findings before readiness, may not approve, and stops on a failing check ([review-change][ref-review]) | **Retain** | A rule now ("never report unexecuted checks as passed"), an acceptance criterion in M2, and never the implementer's own summary |
| Cost-aware model roles | `planner`/`implementer`/`reviewer`/`fixer` resolve to reusable profiles; `model: null` inherits the harness default; escalation is trigger-specific; no price table ([execution.yaml][ref-exec]) | **Adapt**, reject the resolver | The four roles and the two-attempt escalation rule are documented guidance ([agent configuration](../reference/agent-configuration.md), [why agent configuration stays native](agent-independence.md)); there is no shared role-to-model schema, no routing CLI and no invented pricing |
| Human approval | Agents may not record approval; the human merge is the approval boundary; hooks must not approve ([AGENTS.md][ref-agents], [review-change][ref-review]) | **Retain** | Tags, credentials, deployments and releases are human actions, and a future orchestrator executes approvals without ever manufacturing them ([vision](../vision.md)) |
| Worktrees | One task per worktree, explicit claim and release, removal refuses dirty or unmerged work ([AGENTS.md][ref-agents], [worktree tests][ref-worktree-tests]) | **Defer** to M3 | Git worktrees are adopted when parallel delivery needs them; no claim tool is written before that |
| Recovery | Task, branch, worktree and claim persist "while the conversation does not"; a fresh session resumes from derived state ([implement-change][ref-implement], [handoff tests][ref-handoff-tests]) | **Adapt** as a constraint | M2 must recover from a forced interruption with no lost state; run state belongs to one durable owner, never to a chat session |
| Template updates | Native `copier update` with ownership rules that preserve product-owned files, proven by a golden-path test ([template-architecture.md][ref-arch], [update test][ref-update-test]) | **Retain** | Native `copier update` plus the two-revision lifecycle test in `tests/`; no custom update command and no version table |
| Capturing recurring failures as guardrails | "Prefer executable guardrails over durable documentation, and durable documentation over agent instructions" ([capture-learning][ref-capture]) | **Adapt** | The principle becomes an M1 acceptance criterion; the v0.1 evidence that it works is the six named failure modes, each of which fails the check for its own reason |

## Deliberately not migrated

Each item below is a real implementation in the reference repository. Each one is
rejected here because keeping it would create a second owner for something that
already has one, or would pre-empt a decision the roadmap defers.

| Not migrated | Evidence | Why not |
|---|---|---|
| Task manager and workflow state machine | `project/state.yaml`, `project/tasks/*.md`, `tools/project.py` and the `project_tool` package ([template-architecture.md][ref-arch]) | OpenSpec already owns approved specifications and change tasks; a second state machine would drift from it |
| Policy resolver | [execution.yaml][ref-exec], `agent-route`, `template/tools/agent_execution.py` ([`.agents/README.md`][ref-agents-readme]) | Model selection is user-level configuration in each harness; a resolver adds a schema to maintain and still cannot enforce anything |
| Generated dashboard and board sync | `project/board.md`, `make project-status`, `make sync-project-docs` ([template-architecture.md][ref-arch]) | A dashboard is a future orchestrator's surface (M2, M4), not a Markdown block generated by a template |
| Lifecycle hooks | `.agents/hooks/post-task.py`, `make agent-pre-task` / `agent-pre-review` / `agent-post-task` ([`.agents/README.md`][ref-agents-readme]) | The hooks exist to protect the state machine; without it they would only add ceremony |
| Managed lifecycle skills | `.agents/managed/skills/assess-project-state`, `choose-next-task`, `prepare-task`, `complete-task`, `reassess-project` ([`.agents/README.md`][ref-agents-readme]) | They encode the rejected task lifecycle |
| Render matrix | `docs/profile-matrix.md` and one golden-path test per combination ([template-architecture.md][ref-arch]) | A matrix multiplies maintenance for combinations no project uses; ai-devkit adds one profile per real need |
| Release automation for generated projects | `tools/template_release.py`, two-phase prepare/tag flow ([`.agents/README.md`][ref-agents-readme]) | Creating tags is a human action here; publishing a release is not something a template should do to a product repository |
| Mirrored agent layer | `.codex/`, `template/.agents/`, `template/.codex/` plus `make sync-agent-layer` ([AGENTS.md][ref-agents]) | OpenSpec generates its own harness integrations; a hand-maintained mirror is a second owner that drifts |

## What this review changed here

- **`AGENTS.md` stays an engineering contract.** The reference's "Required Start"
  runs commands before an agent may read anything. That is a workflow protocol
  with its own tooling behind it; `ai-devkit` keeps the intent — read only what the
  task needs — and refuses the protocol.
- **Verification stays one command.** The reference separates focused checks, one
  local pre-review gate and asynchronous exhaustive CI. Here that separation is an
  operating principle in the engineering rules, not a set of Make targets, because
  `mise run check` is cheap enough to remain a single gate at this size.
- **Provenance has one owner.** Copier's answers file records the generating
  revision; there is no devkit version table and no devkit update command.
- **The future orchestrator is evaluated, not ported.** The reference's experience
  is the evaluation criterion — durable derived state, bounded retries, approval
  that only a human can produce, worktree isolation, recovery in a fresh session —
  and not a code base to bring across.

## What would change this page

- If an evaluated orchestrator already provides a deferred capability, that
  `Defer` becomes `Delegate` and the devkit configures it.
- If M1 evidence shows context cost is dominated by repeated rediscovery, the
  tiered-loading lesson becomes an approved change instead of a principle.

## Limits of this review

- Documentation, configuration and test names were reviewed; behavior was not. No
  run of `_ai_project_template` reproduces any guarantee claimed here.
- One project, one stack and one harness line is a narrow evidence base;
  conclusions may not generalize.
- Pinning the commit keeps the evidence auditable, and also means this page ages.

See [the product vision](../vision.md), [the roadmap](../plans/roadmap.md),
[ADR 0001](decisions/0001-minimal-devkit.md),
[OpenSpec, AGENTS.md and ADRs](openspec-and-agents.md) and
[the agent configuration reference](../reference/agent-configuration.md).

[ref-arch]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/docs/template-architecture.md
[ref-agents]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/AGENTS.md
[ref-agents-readme]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/.agents/README.md
[ref-context]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/.agents/context-map.yaml
[ref-exec]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/.agents/execution.yaml
[ref-implement]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/.agents/skills/implement-change/SKILL.md
[ref-review]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/.agents/skills/review-change/SKILL.md
[ref-capture]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/.agents/skills/capture-learning/SKILL.md
[ref-worktree-tests]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/tests/test_project_tool_worktrees.py
[ref-handoff-tests]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/tests/test_agent_handoff.py
[ref-update-test]: https://github.com/Semtexcz/_ai_project_template/blob/d035235c09cf057665cdc526acffa231724b9614/tests/test_copier_update_golden_path.py
