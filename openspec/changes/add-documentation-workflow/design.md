# Design

## Context

See [proposal.md](proposal.md) for motivation and scope, and
[research.md](research.md) for upstream evidence. This design is proposed, not
implemented or approved for application.

Baseline inspected at `f6fffbb111f80fa49474a8db467458b5993addb8`:

- `AGENTS.md`, `docs/vision.md` and ADR 0001 assign standards to ai-devkit,
  product documentation to each project, sessions to native harnesses, change
  tasks to OpenSpec and future run state/recovery to an unselected orchestrator.
- `docs/how-to/review-and-repair-one-change.md` and the
  `evidence-bound-agent-handoff` spec already require separate sessions, exact
  commits, evidence labels, independent verdicts and at most two unsuccessful
  repair attempts. Documentation review must consume that contract.
- `mise.toml` already runs four repository checks, including native OpenSpec
  validation and `uv run --locked zensical build --strict`.
  `zensical.toml` sets `docs/` as the build root. The build is not evidence that
  every command, README link or external URL was checked.
- `.github/workflows/verify.yml`, `tests/test_ci_workflow.py` and the
  `devkit-ci-verification` spec prohibit model calls, credentials, write access
  and source mutation. The generated project's seven checks are a different set.
- `examples/agents/` establishes inert, opt-in examples. `.agents/` and
  `.opencode/` are OpenSpec-owned; the overlay cannot render either. There is no
  devkit-owned skill library or Cezar configuration in this repository.

## Goals / Non-Goals

The design separates policy, authoring and judgment so a project can adopt one
role without a coordinating process. It uses explicit manual handoffs and
existing review records, with measurable evidence of improved correctness.

It creates no runtime, scheduler, documentation database, evidence ledger file,
new task schema or global agent configuration. Local role contracts are inert
examples read explicitly; this change does not resolve installation for all
harnesses or implement future automated phases.

## Decisions

### 1. One standard, two small role contracts

Proposed implementation locations:

| Artifact | Responsibility |
|---|---|
| `docs/reference/documentation-standard.md` | Canonical reusable rubric, severity meanings, evidence rules and pinned external-reference table |
| `docs/how-to/write-and-audit-documentation.md` | Manual invocation, handoff, failure handling and the deferred integration design |
| `examples/skills/README.md` | Explicit-use instructions and ownership warning; no installation command required |
| `examples/skills/documentation-writer/SKILL.md` | Writer inputs, steps, outputs and stop conditions; links to standard |
| `examples/skills/documentation-auditor/SKILL.md` | Independent read-only audit contract; links to the same standard |
| Next numbered ADR in `docs/explanation/decisions/` | Rationale for inert examples, shared policy and optional upstream composition |

The new `examples/skills/` subtree extends the existing inert-example convention;
it is not an active harness discovery directory. Each example uses portable
`name`/`description` front matter and ordinary Markdown. References resolve from
the example location, without host paths. A project may explicitly ask its agent
to read the example and linked standard; copying it elsewhere later requires
deliberately rebinding those links. No skill installation or symlink is needed
for the manual MVP. A short trigger link in `AGENTS.md` points to the standard;
it does not restate policy there. Document ownership explicitly before adding
these examples; never place devkit-owned files in OpenSpec-generated directories.

| Concern | Authoritative owner |
|---|---|
| Reusable standard, role examples and compatibility trials | ai-devkit |
| Repository-specific facts, docs layout, exceptions and documentation review | Adopting project and its maintainers |
| Generic third-party guidance and revisions | Each upstream component |
| Approved scope and implementation checklist | OpenSpec |
| Sessions, tool permissions and credential handling | Native harness and execution environment |
| Evidence from builds, links, tests and schemas | Existing project tools and CI |
| Retry execution state, scheduling, waiting and restart recovery | Human in Level 1; selected orchestrator only in a separately approved Level 2 |
| Policy acceptance, milestone approval and consequential actions | Human |

Alternative: installing a whole external writing/audit framework. Rejected for
the MVP because inspected candidates mix responsibilities, assume unrelated
tooling or conflict with read-only review. Role examples add only the integration
contract; reuse upstream genre and prose references without copying their full
implementation or tool suite.

### 2. Reference-only composition with explicit conflict handling

Use the preferred components and immutable sources in the research. Open only
the selected reference needed for a document type; upstream execution workflows,
hooks, automatic commits, exports and installers are not invoked. The local
contract covers impact assessment, evidence, immutability and handoff; it does
not reproduce a generic writing manual.

Both roles read the same project rules and standard revision. Project-specific
approved exceptions must be explicit and visible to both. External suggestions
are advisory and cannot override project facts, authority or scope. If a project
rule and the reusable contract materially conflict, report the conflict and stop
the affected action for a human decision; do not let Writer and Auditor silently
apply different rubrics. A demonstrable implementation/spec mismatch is reported,
not resolved by rewriting either side to hide it.

Pin selected references individually in a normal documentation table, not a new
package manager or synchronization format. No new runtime dependency is needed.
Unavailable optional references are disclosed; neither role requires a live
network connection once its local contract and standard are available. A future
redistribution requires exact-path licensing and notice review first.

### 3. Shared documentation standard scales by reader need

The implementation will put the following rules in the canonical standard, with
the role examples linking to it rather than repeating it:

| Topic | Proposed rule |
|---|---|
| Information architecture | Start with audience and reader task. Use tutorial, how-to, reference and explanation where useful; README sections can serve several needs. Do not force ADRs, changelogs or agent instructions into a quadrant. No mandatory tree, site or set of empty pages. |
| Responsibility and atomicity | Give each document one clear primary responsibility. Split when a distinct audience or task earns another page, not to hit a size threshold. |
| Single source of truth | Link to the authoritative owner for requirements, facts, rationale and policy. Summaries give context and link back; generated reference links to its schema/source and regeneration command. Do not hand-edit generated material. |
| Progressive disclosure | Put the goal, prerequisites and main decision or working path first. Put optional detail behind descriptive, triggered links; keep adjacent caveats beside the instruction they qualify. |
| Technical evidence | Verify claims using implementation, executable tests, schemas, configuration or captured results at an identified revision. Specifications establish intended behavior; source establishes implementation. Repeating another document is not verification. Mark inference, plans and illustrative output explicitly. |
| ADRs | Follow the repository's numbering and location. Record status, date, context, decision, consequences and alternatives for significant durable decisions. Preserve accepted history; supersede with links when the decision changes. No ADR for ordinary prose edits. |
| Links | Use descriptive internal links relative to the repository's conventions and validate target files/anchors. Prefer primary external sources; pin version-sensitive evidence. Record unreachable external URLs as unverified when failure may be transient. |
| Lifecycle and ownership | The owner of a changed interface or workflow checks its docs in the same change. Use existing reviewer/maintainer ownership; do not invent contacts, mandatory owners metadata, dates or freshness timers. Retire obsolete instructions with migration context and repair inbound links. |
| Development updates | Assess impact from the diff and relevant usage paths. Update affected docs, examples, references, ADRs and agent instructions only when justified; no documentation change is a valid evidenced outcome. Keep plans visibly separate from shipped behavior. |
| Agent-facing text | Keep always-loaded instructions short: non-obvious repository constraints, authority boundaries, verified commands and conditional pointers. Avoid copying inventories, plans or facts discoverable cheaply in source; retain essential safety and completion conditions. |
| Concision | Remove repetition, empty claims, unexplained jargon and low-information stock prose when reader benefit is demonstrable. Preserve useful detail and the author's voice. Neither punctuation preference, word count nor a heuristic score proves a defect or AI authorship. |

For a small script, a README with clear sections may be enough. A larger project
can organize pages by reader task using its existing structure. Reusable guidance
stays separate from the adopting project's content; adopting this standard does
not copy ai-devkit's vision, roadmap or ADR history into that project.

### 4. Writer assesses impact before editing

Inputs: approved task, repository/revision or explicit working diff, intended
reader, requested documentation scope and any supplied findings. The Writer
reads project instructions, existing docs, manifests and task definitions, then
traces affected interfaces, implementation, tests and schemas. Discovery is
bounded by the change; no repository-wide rewrite is implied.

The impact result is `update`, `no-update` or `needs-decision`, with affected
documents and evidence. A code-only internal refactor may justify `no-update`;
a default/flag change with no Markdown diff can require an update. No-match text
search alone is insufficient to decide that documentation is absent or unaffected.
Unresolved public behavior or scope conflicts produce `needs-decision`.

For `update`, make the smallest useful edit, preserving existing correct content.
Support README, architecture explanations, API/CLI references, tutorials, how-to
guides, ADRs and agent instructions by selecting only the relevant reference.
Trace command flags and prerequisites to their owner; run examples only when
authorized and safe, otherwise record source verification and what was not run.
Do not execute a command merely because it appears in a document. Generated docs
use their existing generator only within authorized scope.

Output: impact decision and evidence; changed files or explicit no-op; claims
checked and their provenance; exact verification commands/results; skipped checks
and unknowns; findings addressed; changelog decision. Put evidence in the existing
handoff, not process narration in end-user documentation. Writer self-review does
not substitute for the Auditor.

### 5. Auditor is independent, scoped and immutable

Inputs: scope, base/head or explicit working snapshot, shared-standard revision,
project exceptions and relevant deterministic evidence. A new session reads the
diff and commit list before the Writer summary, then independently locates code,
tests, schemas and relevant linked docs. It receives no Writer transcript or
private reasoning. A standalone full audit accepts an explicit file/directory
scope; a change audit checks affected documentation even when none was edited.

Run with native read-only permissions where available, without write-capable
connectors. Report only in the response or the caller's existing review record;
the caller, not the Auditor, stores the report. Do not edit, format, install,
commit, create a ledger or run builds/tests that write anywhere in the repository.
Consume supplied check output or inspect commands as text; missing build evidence
cannot be manufactured by running a mutating check. Capture before/after content
and status outside the audited tree during trials, including untracked files and
ignored content as needed; Git diff alone would miss newly created files. An
immutable mount is preferable when the chosen backend cannot enforce read-only.
If it cannot be provided, report inability to meet the contract and stop.

Check correctness, missing coverage, drift, contradictions, duplicate owners,
links, commands, structure, terminology and reader usability. Continue feasible
content analysis if build evidence is failed or missing, clearly limiting the
outcome. Confirm suspected defects with evidence; separate uncertain observations
and say what would resolve them. Avoid mechanically grading category, punctuation
or vague personal style preferences.

Each finding has the following report shape; these are report fields, not a
serialized workflow or task-state schema:

```text
ID: DOC-1
Severity: P0 | P1 | P2 | P3
Status: confirmed | uncertain
File: path/to/document.md
Location: line number or named section (plus reviewed revision)
Issue: observed claim or gap, expected behavior and reader impact
Evidence: source/test/schema path:line or command and captured result
Recommendation: smallest concrete correction or verification needed
```

For missing documentation, name the expected existing destination/section or
affected interface and explain why coverage is needed. A report also states scope,
revision, standard, coverage, deterministic evidence, limitations, blocking
findings and a verdict. No findings is stated explicitly when applicable.

| Severity / outcome | Meaning and progression rule |
|---|---|
| P0 | Confirmed instructions expose secrets, cause destructive loss or similarly immediate serious harm. Stop use of the affected procedure and escalate immediately. |
| P1 | Confirmed material error or omission blocks a documented primary task, misstates a public contract or claims unimplemented functionality is available. Blocks progression to readiness. |
| P2 | Confirmed localized defect with a viable workaround or limited impact, such as a secondary broken link or confusing duplicate. Non-blocking, retained for human disposition. |
| P3 | Evidence-backed small usability issue. Advisory; preference-only nits are omitted. |
| `PASS` | Agreed audit scope completed, required deterministic evidence available and passing for the candidate, no confirmed P0/P1 and no unresolved uncertainty that prevents judging a primary task or safety claim. P2/P3 may remain, explicitly listed. |
| `FAIL` | Any confirmed P0/P1, or a failed required deterministic check for the candidate. |
| `INCOMPLETE` | Missing material evidence, failed isolation, tool failure or an unjudgeable potentially consequential claim. Blocks readiness without asserting a confirmed defect. |

Uncertain findings do not acquire confirmed severity by repetition. Rank their
potential impact provisionally and keep them separate from confirmed counts.
An unreachable optional external URL can remain an uncertainty without blocking
a completed local-scope audit; an unverifiable installation instruction cannot.
Materiality and required checks are agreed before audit using the project's
existing verification contract. An intentionally README-only repository has no
invented site-build requirement. Audit verdicts are technical evidence, never
human approval.

### 6. Three integration levels, with only the manual MVP in scope

**Level 1 — manual, proposed implementation scope.** Either role can be invoked
alone. For a development change, a person coordinates impact assessment, Writer
only if needed, deterministic project checks outside the Auditor, then a fresh
Auditor. A `no-update` decision still receives an independent impact check when
the workflow is used; it does not mandate a repository-wide audit on every commit.

The handoff uses `evidence-bound-agent-handoff`: final review requires a clean,
committed candidate with exact base/head SHAs. Uncommitted audits are preliminary
and record their snapshot limitations. Record reports in the existing issue,
review or change discussion, not a second task list. Map audit `PASS` to supporting
evidence for `APPROVE`; `FAIL` and `INCOMPLETE` support `REQUEST CHANGES`. A PASS
alone cannot approve the entire software change.

For remediable blocking findings, return exact IDs and evidence to Writer, rerun
affected checks and independently audit the new candidate. Use the existing
two-unsuccessful-attempt bound across the encompassing change, not two additional
attempts for each skill. Stop after the second unsuccessful return to review;
P0, scope/architecture conflicts, unavailable evidence and isolation failures
escalate immediately instead of consuming speculative repair attempts. Report
remaining findings and exact evidence at exhaustion. Cosmetic P2/P3 do not trigger
unbounded polishing. Head changes invalidate prior final evidence. Track attempts
in the existing human handoff record; add no durable run-state store.

**Level 2 — future agent workflow, separate approval.** Preserve the same
assessment → optional Writer → deterministic checks → fresh Auditor → bounded
repair sequence. The orchestrator receives outcome and findings, controls the
budget, persists attempts/pending questions and resumes interrupted work. Skills
remain stateless. Missing/malformed reports, missing verdicts and timeouts must
stop or escalate, never default to success. Audit the actual current candidate on
recovery; reuse a completed result only for matching revision, scope, standard
and evidence. No duplicate task checklist or state file is introduced.

Cezar is an optional candidate, not an ai-devkit dependency. Its inspected native
graph nodes can express an assessment agent with update/no-update/needs-decision
verdicts, conditional Writer, existing shell checks, an Auditor with
pass/fail/incomplete verdicts, a bounded loop and a human gate. Wire every failure,
missing-verdict and exhausted branch explicitly. Native loop counters own the
repair bound; do not stack skill-level retries. Re-audit with fresh sessions on
every cycle; do not use `session.continue` from Writer or reuse an earlier Auditor
session. Store findings in native run output or existing review artifacts and
pass them by native node-output references, not a custom parser or engine change.

Before approving a Cezar configuration, demonstrate on a pinned supported release:
fresh audit context, enforced immutable source, complete finding transfer and
verdict parsing, a no-update path, two failed repairs, cancellation, and recovery
after interruption at Writer, check, audit and human-wait boundaries. The current
source and documentation are not a tested stable-release integration. Documented
Ask/read-only naming and backend tool allowlists are insufficient proof of
immutability. Use existing harness/container restrictions or keep coordination
manual if safe isolation cannot be expressed. Never weaken sandboxing or approval
boundaries to make the workflow run. No Cezar engine extension is justified by
this research; a demonstrated gap would require a separate decision.

**Level 3 — deterministic CI, separate approval for additions.** Reuse today's
strict documentation build and OpenSpec validation. Inventory exact build-root
coverage first. If uncovered README paths, referenced files or anchors warrant a
new check, evaluate a maintained tool (for example a link checker) rather than
implementing a custom parser. Pin it through existing dependency owners and expose
the same non-mutating command locally and in CI. Do not add a check until a real
capability and meaningful broken fixture establish its behavior. Tests must prove
failure on broken input, success on corrected input and no tracked-file mutation.

Local links and builds are deterministic gates. Live external URLs can fail from
network, rate limits or redirects; use bounded opt-in/scheduled reporting with
documented exclusions and distinguish transport failure from a confirmed dead
link. Do not make new network checks a default PR gate without evidence. Subjective
LLM auditing stays outside CI; preserve `contents: read`, no model calls, no secret,
no privileged PR trigger and no publication. No CI/dependency changes in this MVP.

## Acceptance criteria and verification strategy

The delta specs define behavioral contracts. The following trials verify the
future manual implementation without claiming deterministic proof of LLM quality.
Use throwaway repositories/fixtures outside production sources; a human compares
observed reports with planted defects. Never execute the upstream scripts merely
to validate a role example.

| Trial | Expected evidence | Task |
|---|---|---|
| README-only internal refactor | Writer gives evidenced no-update; files unchanged; Auditor independently agrees | 3.1 |
| CLI default/flag changed, docs untouched | Impact assessment finds affected guide/reference; minimal verified edit; stale claim detected independently | 3.2 |
| Genre coverage | Explicitly invoke each role contract; exercise README, architecture, API/CLI reference, tutorial, how-to, ADR and agent instructions with applicable scope | 3.3 |
| Mixed seeded audit | Detect stale/default error, absent prerequisite, contradiction, duplicate owner, broken link, bad command and obstructive filler; preserve correct prose | 3.4 |
| Uncertainty and gating | Demonstrate PASS with non-blocking P2/P3, FAIL with confirmed P1, INCOMPLETE for material missing evidence and prompt escalation for P0 | 3.4 |
| Immutability and independence | New session has only handoff/repository evidence; attempted write denied by environment; complete before/after snapshot unchanged | 3.5 |
| Disagreement and bounded repair | Shared-rule conflict escalates; exact finding IDs returned; two unsuccessful repairs stop; changed head requires fresh review | 3.6 |
| Optional reference unavailable | Mandatory core workflow still works, absence disclosed, no installer or unreviewed script run | 3.6 |
| Repository consistency | Native change/all-spec strict validation and `mise run check` pass; no unintended source mutation | 4.2 |

For seeded technical defects, acceptance requires every planted blocking defect
to be found with source evidence, zero unsupported confirmed blockers, complete
finding fields and zero Auditor writes. Assess stylistic examples for reader
impact, not exact wording or AI-origin detection. Record fixture revision, scope,
role/standard revision, executed commands, outcomes, false positives and omissions
in the existing review record. Failed trials block declaring the manual MVP
complete. These trials are not performed by the current proposal task.

The current proposal is verified by native OpenSpec validation, cross-artifact
review and `mise run check`, plus a working-tree boundary check. The docs build
does not cover files under `openspec/changes/`, so proposal links also need direct
inspection. No overlay/integration behavior changes; `test-template` is not
required for this proposal.

## Risks / Trade-offs

- External prompts change or disappear → immutable references, independent pins,
  optional use and manual diff review on upgrades; no automatic synchronizer.
- Upstream text conflicts with local authority → reference-only composition,
  shared rubric and explicit escalation, not raw workflow invocation.
- License ambiguity and bundled examples → no kernel-docs redistribution;
  verify exact files/notices before any future copying.
- Read-only prompt mistaken for enforcement → native restrictions/immutable
  source plus snapshot checks; reject configurations that cannot enforce it.
- Shared standard biases both roles → Auditor independently derives facts from
  source and tests; human evaluates seeded defects and unsupported blockers.
- LLM omission or over-editing → bounded scope, no-op case, seeded trials and
  meaningful evidence; no claim that a prose score proves correctness.
- Inert examples require explicit reading and links → small adoption cost;
  avoids prematurely choosing installation ownership for every harness.
- Audit evidence becomes stale → exact revision binding and re-audit after
  changes; no automatic acceptance from a previous head.

## Migration Plan

After human approval, implement only the manual standard, examples and procedure,
record the ownership ADR, add navigation/discovery links and run the trials.
Existing repositories opt in by reading the standard and invoking either role;
retain their layout and correct content, adopting broader coverage only when
needed. No generated-project update or Copier migration is required.

Rollback removes the optional examples and their discovery/navigation links;
project-owned documentation edits remain reviewed project content. No runtime
state, credential or database migration exists. Agent coordination, installed
skill distribution and new CI checks each need separate approved changes.

## Open Questions

These decisions do not prevent reviewing the manual design:

- Human review: accept the proposed ownership ADR and inert examples before any
  implementation request. This proposal does not itself approve an M1 milestone.
- If redistribution is desired later, which exact upstream assets and notices
  are accepted, and can kernel-docs establish an explicit skill license? The MVP
  works without redistributing any external component.
- Which real project should pilot Level 2, which orchestrator/release (if any)
  should be selected, and can its chosen backend prove enforced immutable audits?
  These determine a later proposal, not this change's tasks.
- Does real adoption expose local-link coverage gaps large enough to justify a
  maintained link checker? Select its version and network policy only then.
