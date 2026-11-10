# documentation-auditing Spec Delta

## Purpose

Provide independent, read-only verification of project documentation and an
evidence-based gate for bounded remediation within the existing change handoff.

## ADDED Requirements

### Requirement: Audit uses independent context and immutable files

The Auditor SHALL use a separate session, inspect repository evidence independently
and never modify repository files. It SHALL NOT inherit Writer session state,
install tools or run repository-writing commands. If immutable execution cannot
be provided, it SHALL stop and report an incomplete audit.

#### Scenario: Audit after writing

- **WHEN** the Auditor receives a Writer handoff
- **THEN** it inspects the actual diff and commit list before relying on the summary, uses the shared standard and verifies claims against source and tests without the Writer transcript

#### Scenario: Read-only guarantee

- **WHEN** the audit runs
- **THEN** repository files, including untracked and ignored content, remain unchanged and the report is returned to the caller instead of written into the repository

#### Scenario: Missing build output

- **WHEN** build evidence is missing and the build would write repository artifacts
- **THEN** the Auditor reports the missing evidence, continues feasible read-only analysis and does not run the build itself

### Requirement: Audit checks accuracy and necessary coverage

The Auditor SHALL check agreed-scope documentation against relevant implementation,
tests, configuration and schemas for stale, incorrect, missing, contradictory or
duplicated information. It SHALL inspect links, commands, structure, terminology
and readability and distinguish confirmed defects from uncertain observations.

#### Scenario: No documentation diff

- **WHEN** code changes invalidate documentation that was not edited
- **THEN** the change audit examines the affected documentation and reports the mismatch even if the Writer reported no-update

#### Scenario: Standalone audit

- **WHEN** the user supplies an explicit file or directory scope without a Writer run
- **THEN** the Auditor can audit that scope independently and names its coverage and evidence limits

#### Scenario: Search is inconclusive

- **WHEN** a claim is not found by an initial text search
- **THEN** the Auditor traces relevant entry points, tests or schemas before confirming a mismatch and otherwise reports uncertainty and what evidence would resolve it

#### Scenario: Verbosity with reader impact

- **WHEN** repeated explanations or vague stock prose obscure a required instruction
- **THEN** the Auditor cites the passage, explains the reader impact and recommends a concrete reduction without claiming AI authorship or applying preference-only nits

### Requirement: Findings are actionable and evidence-bound

Every finding SHALL include an ID, P0–P3 severity, confirmed or uncertain status,
file, line or section, observed and expected behavior, reader impact, supporting
evidence and recommended remediation. The report SHALL identify reviewed revision,
scope, standard, coverage, check evidence and limitations.

#### Scenario: Confirmed defect

- **WHEN** documentation states an incorrect CLI default
- **THEN** the finding identifies the documentation location and conflicting implementation or test evidence and recommends the smallest correction

#### Scenario: Missing information

- **WHEN** a primary documented task omits a necessary prerequisite
- **THEN** the finding identifies the expected destination or affected interface, evidence of the prerequisite and how the omission prevents the task

#### Scenario: No findings

- **WHEN** the scoped review finds no defects
- **THEN** the report explicitly states No findings while still identifying coverage and verification limitations

### Requirement: Audit has meaningful progression gates

Confirmed P0 serious-harm instructions and P1 primary-task or public-contract
defects SHALL block readiness; P2 localized defects and P3 minor usability issues
SHALL be non-blocking. The Auditor SHALL return PASS, FAIL or INCOMPLETE and SHALL
NOT treat material missing evidence, failed checks or an uncertain critical claim
as a successful audit.

#### Scenario: Blocking defect or deterministic failure

- **WHEN** a confirmed P0/P1 remains or a required deterministic check fails for the candidate
- **THEN** the verdict is FAIL, blocking findings are separated from non-blocking observations and P0 prompts immediate human escalation

#### Scenario: Passing with limited findings

- **WHEN** the agreed audit scope is completed, required checks pass and only confirmed P2/P3 or non-material observations remain
- **THEN** the verdict is PASS with remaining findings explicitly listed, without implying human acceptance

#### Scenario: Incomplete verification

- **WHEN** material evidence is unavailable, isolation fails, a tool prevents required coverage or a potentially consequential claim cannot be judged
- **THEN** the verdict is INCOMPLETE, readiness is blocked and the report names what is needed without inventing a confirmed defect

#### Scenario: Optional external URL unavailable

- **WHEN** a nonessential external link cannot be reached because of an uncertain network failure
- **THEN** the Auditor distinguishes the uncertainty from a confirmed dead link and does not turn it into an unsupported blocking defect

### Requirement: Manual remediation preserves existing handoff bounds

The manual procedure SHALL return exact findings to the Writer, rerun relevant
checks outside the Auditor and independently audit each corrected candidate.
It SHALL use the existing two-unsuccessful-repair bound for the whole change and
existing records, without a new tracker, retry engine or workflow state file.

#### Scenario: Second unsuccessful repair

- **WHEN** the second repair returns to review with an unresolved blocker
- **THEN** coordination stops and escalates remaining findings and evidence to the human without starting a third attempt or resetting the bound for another role

#### Scenario: Non-remediable failure

- **WHEN** the workflow encounters a scope conflict, unavailable material evidence or failed isolation
- **THEN** it stops dependent work and escalates the limitation instead of initiating speculative repair loops

#### Scenario: Changed candidate

- **WHEN** a repair changes the reviewed head
- **THEN** final review and required checks apply to the new clean committed candidate, and earlier results do not transfer automatically

#### Scenario: Preliminary working-tree audit

- **WHEN** an audit covers uncommitted edits
- **THEN** its report identifies that snapshot as preliminary and does not replace the final clean, commit-bound independent handoff

### Requirement: Audit remains manually usable and technically distinct from approval

The Auditor SHALL work by explicit invocation without Writer, orchestration,
installation or a particular agent. Its outcome SHALL support the existing review
verdict rather than replace software review or human authorization. Proposed
automated integration SHALL retain existing state and deterministic CI owners.

#### Scenario: Verdict handoff

- **WHEN** the documentation audit is handed to final change review
- **THEN** PASS supplies supporting evidence for APPROVE while FAIL or INCOMPLETE supports REQUEST CHANGES, and consequential actions remain subject to human approval

#### Scenario: Future automation

- **WHEN** documentation coordination or CI extensions are considered
- **THEN** they require separate approval, retain orchestrator-owned recovery and retry state, and do not put subjective model auditing into deterministic CI
