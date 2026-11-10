# documentation-authoring Spec Delta

## Purpose

Define a reusable Writer that decides whether documentation work is necessary
and maintains accurate project documentation with minimal justified edits.

## ADDED Requirements

### Requirement: Impact assessment precedes writing

The Writer SHALL inspect relevant repository instructions, documentation,
implementation, configuration, tests and schemas before editing. It SHALL report
update, no-update or needs-decision with evidence and affected documentation,
including documentation affected by code changes without a documentation diff.

#### Scenario: Internal refactor

- **WHEN** changed implementation preserves documented interfaces and workflows
- **THEN** the Writer can return no-update with evidence and leaves documentation unchanged

#### Scenario: Changed default without documentation edits

- **WHEN** a changed CLI default invalidates an existing example
- **THEN** the Writer identifies the affected reference or guide and proposes the necessary correction

#### Scenario: Ambiguous behavior

- **WHEN** a public behavior or approved-scope conflict cannot be resolved from authoritative evidence
- **THEN** the Writer reports needs-decision and stops the dependent edit without inventing behavior

### Requirement: Technical claims are evidence-bound

The Writer SHALL verify technical claims against authoritative repository
evidence, distinguish current behavior from intent, plans and inference, and
record verification limits. It SHALL NOT fabricate commands, output, interfaces,
owners or capabilities, or treat another document as proof of implementation.

#### Scenario: Command cannot safely run

- **WHEN** an example has side effects outside authorized scope
- **THEN** the Writer inspects its source, flags and prerequisites without executing it, states what was not run and does not claim runtime verification

#### Scenario: Missing evidence

- **WHEN** no evidence establishes a claimed capability or sample output
- **THEN** the Writer omits the unsupported claim, labels an explicit inference or illustrative example, or reports the gap rather than presenting it as verified

#### Scenario: Intended and implemented behavior differ

- **WHEN** tests, implementation and an approved requirement reveal a material mismatch
- **THEN** the Writer reports the discrepancy and documents only what the evidence supports without altering scope or hiding the defect

### Requirement: Edits preserve useful documentation

The Writer SHALL make only necessary in-scope documentation changes, preserve
correct existing content and project conventions, minimize duplication and
support README, architecture, API/CLI reference, tutorials, how-to guides, ADRs
and agent instructions using the shared standard.

#### Scenario: Small correction

- **WHEN** a single documented flag is stale
- **THEN** the Writer corrects the affected passage and related necessary references without rewriting unrelated sections or imposing another documentation tree

#### Scenario: Document genre

- **WHEN** any supported documentation genre is requested
- **THEN** the Writer selects its reader need and relevant guidance without adding unnecessary companion documents or conflating planned and implemented behavior

#### Scenario: Generated reference

- **WHEN** the affected reference is generated
- **THEN** the Writer uses the existing authorized generation process or reports the required source change instead of hand-editing generated output

### Requirement: Writer provides a verifiable handoff

The Writer SHALL report its impact decision, changed files or no-op, supporting
evidence, exact checks and results, skipped checks, unresolved questions and
changelog decision through the existing handoff. Its self-review SHALL NOT count
as an independent audit or human approval.

#### Scenario: Completed writing

- **WHEN** the Writer returns its result
- **THEN** a reviewer can identify what changed, why, which claims were checked and what remains unverified without relying on the Writer's session

#### Scenario: Repair request

- **WHEN** the Writer receives confirmed audit findings for remediation
- **THEN** it cites finding IDs, preserves approved scope and reports corrections and verification under the existing repair bound

### Requirement: Manual invocation does not require orchestration

The Writer SHALL be usable independently by explicitly reading its inert role
example and shared standard. Invocation SHALL NOT require skill installation,
global configuration changes, an orchestrator, an upstream script or a specific
harness, model or provider.

#### Scenario: Incremental adoption

- **WHEN** an existing project invokes only the Writer
- **THEN** it can assess and update the requested documentation through its existing agent without enabling an Auditor, CI integration or installed skill collection
