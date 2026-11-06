# Spec Delta

## Purpose

What a native Copier update between two tagged revisions of the ai-devkit overlay must preserve, report and record in a generated project.

## ADDED Requirements

### Requirement: Project-owned work survives an overlay update

An overlay update SHALL leave application code, project tests and Python dependency manifests exactly as the project committed them.

#### Scenario: Edited entry point and its regression test

- **WHEN** a generated project changes `main.py` and adds its own regression test, commits both, and then updates to a newer tagged overlay revision
- **THEN** both files are byte-identical to the committed version and the project still passes its verification command

#### Scenario: Python dependency manifests

- **WHEN** a generated project holds its own `pyproject.toml` and `uv.lock` and updates to a newer tagged overlay revision
- **THEN** neither file changes, because the overlay never renders them

### Requirement: Project-owned documentation and local edits survive

An overlay update SHALL keep documentation the project wrote and documentation the project edited.

#### Scenario: Page the overlay never rendered

- **WHEN** a project adds a documentation page and links it from its documentation entry point, commits the change, and updates the overlay
- **THEN** the page and the link remain, and the strict documentation build still succeeds

#### Scenario: Overlay-owned page edited by the project

- **WHEN** a project edits an overlay-owned page that the newer overlay revision does not change, and then updates
- **THEN** the project's edit remains unchanged

### Requirement: Conflicting edits are reported and resolvable

An overlay update SHALL report a conflict when the overlay and the project change the same region of the same file, and SHALL NOT discard either side.

#### Scenario: Shared rule edited on both sides

- **WHEN** the project and the newer overlay revision both change the same region of `AGENTS.md`, and the project has a clean committed baseline
- **THEN** the update leaves a conflict in the file, the version control system records the file as unresolved, both sides' text is present, and no conflict witness file is left behind

#### Scenario: Resolving the conflict

- **WHEN** the conflict is resolved by hand, staged, and the project is verified
- **THEN** the verification command succeeds and the resolved update can be committed as one change

### Requirement: Provenance advances and nothing else moves

An overlay update SHALL record the applied template revision while leaving unrelated files untouched.

#### Scenario: Provenance after an update

- **WHEN** an update to tagged revision `v0.2.0` completes from a project created at `v0.1.0`
- **THEN** `.copier-answers.yml` records `v0.2.0`, its source path still names the template repository the project was created from, the project's answers are unchanged, and the native tool reports the project as up to date

#### Scenario: Footprint of an update

- **WHEN** the update applies a change to two overlay-owned files
- **THEN** exactly those files and the provenance record differ, and no file is added or removed

### Requirement: Updates run between temporary tags

The update lifecycle SHALL be verified without creating, moving or pushing a release tag of the devkit.

#### Scenario: Fixture revisions

- **WHEN** the lifecycle is verified
- **THEN** both revisions and the generated project live in temporary directories that are removed afterwards, and the devkit working tree is unchanged
