# Spec Delta

## Purpose

What this repository's hosted verification must run, with which permissions, and what it must leave untouched.

## ADDED Requirements

### Requirement: Hosted verification runs the local commands

Hosted verification SHALL run the same commands a developer runs locally, through the repository's own tasks rather than through a copy of their logic.

#### Scenario: Verification command sequence

- **WHEN** the workflow runs for a push to `main` or a pull request targeting `main`
- **THEN** it installs the locked toolchain, prints the installed versions, runs the repository checks and runs the generation and update integration test

#### Scenario: No duplicated test logic

- **WHEN** the workflow invokes a check
- **THEN** it invokes the repository's task for that check instead of calling the underlying checker directly

### Requirement: Hosted verification is read-only

Hosted verification SHALL NOT require write access, credentials, model access or privileged execution of pull-request code.

#### Scenario: Permissions

- **WHEN** the workflow is reviewed
- **THEN** repository contents are read-only, no credential or model provider key is referenced, and no privileged pull-request trigger is used

#### Scenario: No publishing

- **WHEN** the workflow completes
- **THEN** it has created no commit, tag, release or push

### Requirement: Third-party actions are pinned

Hosted verification SHALL use only reviewed actions, each pinned to a full commit identifier.

#### Scenario: Action reference

- **WHEN** the workflow uses an action
- **THEN** the reference names a full commit identifier and never a movable tag or branch

### Requirement: Verification leaves tracked files unchanged

A successful verification SHALL NOT modify any tracked file.

#### Scenario: Working tree after both verification tasks

- **WHEN** the repository checks and the integration test have passed
- **THEN** the tracked working tree is unchanged, and only ignored artefacts such as environments, caches and generated documentation exist

### Requirement: Hosted and local results are reported separately

A local test run SHALL NOT be reported as evidence that hosted verification passed.

#### Scenario: Reporting status

- **WHEN** results are reported and the workflow has not executed on the hosting service
- **THEN** hosted verification is reported as pending rather than passed
