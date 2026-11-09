# Review and repair one change

A procedure for handing one change from an implementation agent to an independent
reviewer, then to a bounded repair agent, and finally to a human. It is
harness-agnostic: use OpenCode, Codex, Cline or another agent, or do a stage
yourself. The record lives in the repository, the pull request and the project's
checks — never in a new JSON or YAML state file.

This is a human-coordinated procedure, not autonomous delivery. The agents perform
the stages; the human owns approval.

## Before you start

- One approved OpenSpec change, or equivalent project-owned scope, exists. Its
  `proposal.md`, delta spec and `tasks.md` define what may change.
- The implementer and the reviewer use separate sessions. The reviewer must not
  inherit the implementer's context or trust its summary.
- The repository is the only source of truth for code and diffs; the project's
  checks and CI are the only source of automated verification.
- Agree where the handoff record goes: the pull-request description, the review
  request, or the change's issue. Do not create a second task list.

## Handoff 1: implementation to review

The implementer supplies all of the following. A reviewer may reject an incomplete
handoff without reading the diff.

| Field | Required content |
|---|---|
| Approved scope | OpenSpec change name and path, or the project-owned scope, with a link to its proposal, spec and tasks |
| Repository and branch | Repository identity and the branch under review |
| Commits | Exact full base and head commit SHAs, not abbreviated or branch names |
| Working tree | Clean: no uncommitted or untracked paths, and every in-scope change committed in the head |
| Changed files and exclusions | Files that changed, and a short list of what the change deliberately does not touch |
| Verification | Each exact command, its result, and every check skipped with the reason. A check that did not run is never reported as passed |
| Compatibility | When a public interface changes: callers checked, whether existing implementations still satisfy the contract, and the migration or deprecation position |
| Release decision | Whether a changelog entry or version change is required, the entry made, or the reason none is required |
| Known limitations | Unresolved behavior, platform gaps and claims that were not verified |
| Usage and cost | Model and provider usage from harness reporting and its cost, or an explicit "unavailable" |

Label every claim by provenance: `verified`, `self-reported` or `unavailable`. A
verified claim names the commit, command output or CI run that establishes it. See
[evidence labels](#evidence-labels).

Committing requires whatever authorization the project specifies; an implementer
does not commit on its own merely to satisfy this procedure. A reviewer may examine
uncommitted changes as a preliminary review, but the final independent review is
commit-bound: `git diff <base>..<head>` excludes uncommitted and untracked work, so
the working tree must be clean and every in-scope change committed before that
review starts.

## Handoff 2: review to repair

The independent reviewer:

1. Reads the base-to-head diff and commit list before the summary, for example
   `git diff <base>..<head>` and `git log <base>..<head>`.
2. Reads only the changed files, tests and documentation needed to judge the changed
   behavior. Broad repository reading is not required and is not evidence.
3. Reproduces each important suspected defect when feasible. When it is not
   feasible, says so and explains what would have reproduced it.
4. Reports findings ordered by severity, or states `No findings` explicitly. Each
   finding carries an identifier, a severity, a `file:line` reference, the observed
   and expected behavior, and the reproduction or supporting evidence.
5. Separates blocking findings from non-blocking observations.
6. Ends with exactly one verdict: `APPROVE` or `REQUEST CHANGES`. `APPROVE` is not
   issued while a blocking finding is unresolved.

A compact finding shape:

```text
[blocking] F1 — path/to/file.py:123 — <defect in one line>
Observed: <what happens>
Expected: <what should happen>
Evidence: <command and result, or why reproduction was not feasible>
```

The review record is the findings plus the verdict. A summary that hides the
findings does not satisfy this handoff. A clean review states `No findings` before
`APPROVE`; a reported defect still carries the evidence above.

## Handoff 3: repair to review

The repair agent:

- Starts from the exact review findings and cites the finding identifiers it
  addresses.
- Keeps the original approved scope. New scope is not absorbed into a repair; it
  stops and asks for separate approval.
- Makes bounded corrections and touches only what the findings require.
- Adds a regression test for each confirmed defect. The test fails before the
  correction and passes after it, or the report explains why a test is not
  feasible.
- Reruns the relevant verification and records the exact commands and results.
- Returns a repair report: findings addressed, files and commits changed,
  verification evidence, remaining or unresolved findings, and new risks.

**Repair bound.** A repair attempt counts when it returns to review and a blocking
finding is still unresolved. After the second unsuccessful attempt, stop and
escalate to a human with the findings and verification evidence. Do not start a
third attempt.

## Handoff 4: review to human

A repair produces a new head commit, so the reviewer re-reviews that commit and
repeats the relevant verification. The final handoff to the human contains:

- the exact reviewed commit SHA and the exact merge-candidate SHA;
- the independent review verdict, attached to those commits;
- CI status for the merge candidate: provider, run and the commit it tested;
- remaining risks and non-blocking observations;
- every action still requiring human approval: merge, tag, publish, deploy,
  credential change, or spending beyond an explicit budget.

If the reviewed commit and the merge candidate differ, review and CI run again, or
the difference is escalated. An approval for an earlier commit does not travel to a
later one.

The human decides. An agent may prepare a merge or release, but does not perform a
consequential action without that approval. The ownership and approval boundaries
are recorded in the [product vision](../vision.md#human-approval-boundaries).

## Evidence labels

| Label | Meaning | Test |
|---|---|---|
| `verified` | A repository artifact or run establishes the claim | The reader can re-check the named commit, command output, CI run or review record |
| `self-reported` | An agent or person states it, but no repository artifact establishes it | Say who reported it and what could not be checked |
| `unavailable` | The data was not captured | State it; do not substitute an estimate |

A session transcript is not verification. A polished summary is not verification.
A check that did not run is not a pass.

## Worked example: Bookvoice PR #4

The pilot is [Semtexcz/Bookvoice PR #4](https://github.com/Semtexcz/Bookvoice/pull/4),
merged on 2026-11-07. PR #4 carries more than the bounded feature: it also includes
the project's ai-devkit adoption and environment preparation. The bounded
implementation is the OpenSpec change
`add-proficiency-level-to-llm-interfaces` (TASK-044).

The reported sequence was: DeepSeek implemented the bounded change; Codex found
protocol-compatibility and release-metadata defects; DeepSeek repaired them; Codex
approved the repair; GitHub CI passed; the merge was recorded against the account
`Semtexcz`. The table separates what the repository and GitHub record from what only
the agents reported.

| Claim | Status | Evidence |
|---|---|---|
| DeepSeek implemented the bounded change | `self-reported` | No harness or model metadata is stored in Git or on the PR; the commits are authored under the human GitHub identity |
| Codex found protocol-compatibility and release-metadata defects | `self-reported` | Corroborated by the change's `tasks.md` section 6, which lists protocol restoration (6.1), cache and validation regressions (6.2–6.3), version and changelog (6.4) and re-verification (6.6); the final head contains both legacy and proficiency-aware protocols and the `0.23.0` metadata |
| DeepSeek repaired the findings | `self-reported` | Corroborated by commits `181a261` and `6454ca7`; the latter restores the legacy `dev` extra in `pyproject.toml` |
| Codex approved the repair | `self-reported` | The PR body says "Independent Codex review approved the feature repairs"; GitHub records zero PR reviews and zero comments |
| GitHub CI passed | `verified` | Four `test` check runs succeeded on head `6454ca7917bd55435d3f6cec7c980a3393e11add`; the last completed at 15:08:16Z, before the merge at 15:08:28Z |
| GitHub account `Semtexcz` performed the final merge | `verified` | GitHub records the account event `merged_by: Semtexcz`, merge commit `5b62c6beb8e64f297d80e391254e9904eddf199d`, base `2979ae7ce10e92ccd748750f64a1dcfd7fc0563d` and head `6454ca7917bd55435d3f6cec7c980a3393e11add`; GitHub verifies the account, not the person operating it |
| A human manually initiated the merge | `self-reported` | The pilot's coordinator states it; no repository artifact separates a manual merge from an automated action by the account |
| Model usage and cost | `unavailable` | No harness usage or cost record is stored in the repository or on the PR |

This is one pilot with a human coordinating every stage. It is not evidence of
autonomous delivery, and it is not sufficient evidence to close M1.

## What this procedure does not do

- It does not add an orchestrator, router, scheduler or retry engine.
- It does not add a task-state file, workflow schema or second backlog.
- It does not require a model, provider or harness.
- It does not merge, tag, publish or deploy anything.
- It does not turn a self-report into verification.

A future orchestrator may coordinate these stages, but it must read and write the
same owners: OpenSpec for scope, Git for commits and diffs, project checks and CI
for automated evidence, native harnesses for sessions, and the human for approval.

## Related

- [Configure coding agents](configure-coding-agents.md) — roles and native setup.
- [OpenSpec: commands, generated files and validation](../reference/openspec.md) —
  the change record this procedure consumes.
- [OpenSpec, AGENTS.md and ADRs](../explanation/openspec-and-agents.md) — why
  specifications, rules and change tasks stay separate.
- [Product vision](../vision.md) and [roadmap](../plans/roadmap.md) — the approval
  boundaries and the milestones this pilot does not close.
