# Tasks

## 1. Change definition

- [x] 1.1 Create the change with the native CLI and write the proposal, design and delta spec; verify `openspec validate evidence-bound-agent-handoff --strict --no-interactive` passes
- [x] 1.2 Keep OpenSpec as the only owner of the change record and add no task-state file, backlog or workflow schema; verify the change directory contains only OpenSpec artifacts

## 2. Procedure documentation

- [x] 2.1 Write `docs/how-to/review-and-repair-one-change.md` with the four handoffs and every minimum field; verify each field named in the approved scope is present and the page reads without harness-specific commands
- [x] 2.2 Record Bookvoice PR #4 as one pilot with verified, self-reported and unavailable evidence separated; verify every pilot claim names its evidence or is marked unavailable
- [x] 2.3 State the human-coordinated and non-autonomous boundary and that one pilot does not close M1; verify the statements appear in the how-to

## 3. Documentation integration

- [x] 3.1 Link the how-to from `docs/index.md` and add it to the how-to navigation; verify the strict documentation build resolves both links
- [x] 3.2 Record the user-visible addition under `[Unreleased]` in `CHANGELOG.md`; verify the entry is under Added and is not duplicated

## 4. Verification

- [x] 4.1 Run `mise run check` and confirm every task in the repository check passes
- [x] 4.2 Run `git diff --check` and confirm no whitespace errors
- [x] 4.3 Re-run the strict OpenSpec validation and confirm the change has no warnings

## Workflow follow-up

- Obtain an independent review of the exact head commit from a separate session; the reviewer inspects the diff and returns APPROVE or REQUEST CHANGES.
- If review requests changes, repair only the reported findings, add regression coverage where a defect is confirmed, and return to review; stop after two unsuccessful attempts.
- Re-review the new head commit after any repair and verify CI on the merge candidate.
- The human approves the merge; do not commit, push, publish or archive as part of this change.
- Do not archive this change during the pilot; archive it only after the human accepts the procedure and the pilot evidence.
