# evidence-bound-agent-handoff Specification

## Purpose
What minimum evidence and verdicts a change must carry when it passes from
implementation through independent review and bounded repair to human approval.

## Requirements

### Requirement: Implementation handoff precedes review

Before requesting final independent review, the implementer SHALL supply one
handoff record naming the approved scope, repository and branch, exact base and head
commits, working-tree state, changed files and exclusions, verification evidence,
interface compatibility, release decision, known limitations and usage data. The
working tree SHALL be clean and every in-scope change SHALL be committed in the
named head, under the authorization the project specifies.

#### Scenario: Complete record

- **WHEN** the implementer hands a change to review
- **THEN** the record contains every required field, and no field is blank except one explicitly marked unavailable

#### Scenario: Verification evidence

- **WHEN** a check is reported in the handoff
- **THEN** the record names the exact command and its result, and a check that did not run is listed as skipped with a reason and never as passed

#### Scenario: Clean tree with committed scope

- **WHEN** the head commit is handed to final independent review
- **THEN** the working tree is clean and every in-scope change is contained in the named head commit

#### Scenario: Interface and release decisions

- **WHEN** the change alters a public interface or release metadata
- **THEN** the record states the caller compatibility assessment and the changelog and version decision

#### Scenario: Usage data

- **WHEN** model usage or cost is available from harness reporting
- **THEN** it is reported, and otherwise it is marked unavailable rather than estimated

### Requirement: Review is independent and diff-based

The reviewer SHALL judge the actual committed diff rather than the implementer's
summary, read only context relevant to the changed behavior, reproduce important
suspected defects when feasible, and report findings ordered by severity with file
and line references or state `No findings` explicitly. The final independent review
SHALL be bound to a commit and a clean working tree; a preliminary review of
uncommitted changes SHALL NOT substitute for it.

#### Scenario: Diff first

- **WHEN** review starts
- **THEN** the reviewer inspects the base-to-head diff and commit list before relying on the implementation summary

#### Scenario: Commit-bound review

- **WHEN** the final independent review begins
- **THEN** the working tree is clean and the review covers the base-to-head committed diff

#### Scenario: Actionable finding

- **WHEN** the reviewer finds a defect
- **THEN** the finding names its severity, file and line, observed and expected behavior, and reproduction evidence or why reproduction was not feasible

#### Scenario: Clean review

- **WHEN** the reviewer finds no defects
- **THEN** the review states `No findings` explicitly before issuing APPROVE

#### Scenario: Blocking findings are separated

- **WHEN** findings are reported
- **THEN** blocking findings are listed separately from non-blocking observations

#### Scenario: Verdict

- **WHEN** the findings are reported
- **THEN** the review ends with APPROVE or REQUEST CHANGES, and APPROVE is not issued while a blocking finding remains unresolved

#### Scenario: Independence

- **WHEN** review begins
- **THEN** it uses the handoff record and repository artifacts, not the implementer's session state

### Requirement: Repair is bounded to review findings

A repair agent SHALL receive the exact review findings, keep the original approved
scope, make only bounded corrections, add a regression test for each confirmed
defect, rerun relevant verification and report what changed and what remains
unresolved. After two unsuccessful repair attempts it SHALL stop and escalate to a
human.

#### Scenario: Finding-driven repair

- **WHEN** repair begins
- **THEN** it cites the findings it addresses and changes only what those findings require, and new scope stops for separate approval

#### Scenario: Regression coverage

- **WHEN** a defect is confirmed
- **THEN** a regression test fails before the correction and passes after it, or the repair report explains why no test is feasible

#### Scenario: Repair report

- **WHEN** repair returns to review
- **THEN** it lists findings addressed, files and commits changed, verification commands and results, remaining findings and new risks

#### Scenario: Attempt bound

- **WHEN** a second repair attempt returns with a blocking finding still unresolved
- **THEN** work stops and escalates with the evidence, and a third attempt is not started

### Requirement: Final handoff records verification and human approval

Before merge, release or another consequential action, the final handoff SHALL
name the exact reviewed commit, the independent verdict, CI status for that commit,
remaining risks and the human decision still required. A pending, failed or unrun
CI result SHALL NOT be reported as passed.

#### Scenario: Exact reviewed commit

- **WHEN** the final handoff is prepared
- **THEN** the reviewed head and the merge candidate are named by full commit identifier, and any difference is reviewed and verified again or escalated

#### Scenario: CI on the candidate

- **WHEN** CI passed
- **THEN** the record names the provider run and the commit it tested, and otherwise reports the status as pending, failed or not run

#### Scenario: Repair invalidates earlier approval

- **WHEN** a repair changes the head commit
- **THEN** the final handoff cites a review and CI result for the new commit rather than an earlier one

#### Scenario: Human approval

- **WHEN** the change is ready
- **THEN** merge, tag, publish, deploy, credential change and spending beyond an explicit budget remain pending until a human approves them

### Requirement: Evidence provenance is explicit

Every handoff claim SHALL be distinguishable as verified evidence, an agent
self-report or unavailable data. A verified claim SHALL name the commit, command
result, CI run or review record that establishes it; a summary, session transcript
or assertion SHALL NOT be presented as verification.

#### Scenario: Provenance label

- **WHEN** a handoff reports a result
- **THEN** the result carries one of verified, self-reported or unavailable

#### Scenario: Verified claim

- **WHEN** a claim is labelled verified
- **THEN** it identifies the repository artifact or run that can be re-checked

#### Scenario: Account actions

- **WHEN** a claim about an account action is labelled verified
- **THEN** it states only what the artifact establishes, such as the account that performed the action, not who operated the account or how the action was initiated

#### Scenario: Workflow demonstrations

- **WHEN** a pilot or demonstration is cited as evidence
- **THEN** the record separates repository and CI facts from session-only reports and states whether the workflow was human-coordinated or autonomous

#### Scenario: Missing measurements

- **WHEN** usage, cost or another measurement is unavailable
- **THEN** the record says so and does not present an estimate as measured data
