# Proposal

## Why

A generated project is updated with native `copier update`, and the guide says an
update cannot overwrite project-owned files. That promise was documented but never
executed: no test applied an update between two template revisions, so the boundary
between overlay-owned and project-owned work rested on inspection. Verification had
the same gap — `mise run check` and `mise run test-template` only ran on a
developer's machine, so a clean checkout could break unnoticed.

## What Changes

- Test the native update lifecycle between two temporary tagged template
  revisions: project-owned application code, a project-owned documentation page and
  the project's own edit to an overlay-owned page survive; a same-region edit to
  `AGENTS.md` is reported as a conflict and stays resolvable; `.copier-answers.yml`
  advances without rewriting unrelated files.
- Prove each of the six failure modes the verification contract names — lint,
  format, types, failing test, broken internal documentation link, invalid
  specification — fails `mise run check` for its own reason.
- Add a read-only GitHub Actions workflow that installs the locked toolchain and
  runs the same commands a developer runs: `mise run versions`, `mise run check`
  and `mise run test-template`, then confirms no tracked file changed.
- Correct the overlay's lockfile instructions: committing `mise.lock` without the
  `.mise/locks/` npm sidecar leaves the OpenSpec dependency graph unresolved.

No behavior of a generated project changes, and no new component is introduced:
Copier, mise tasks and GitHub Actions stay the only owners of what they already own.

## Capabilities

### New Capabilities

- `overlay-update-lifecycle`: what a native `copier update` between two tagged
  overlay revisions must preserve, report and record in a generated project
- `devkit-ci-verification`: what this repository's hosted verification must run,
  with which permissions, and what it must leave untouched

### Modified Capabilities

## Impact

- `tests/test_update_lifecycle.py`, `tests/test_ci_workflow.py`, `tests/testkit.py`
  and the negative cases in `tests/test_template.py`; all of it runs behind
  `mise run test-template`
- `.github/workflows/verify.yml` (new)
- `templates/python-script-overlay/template/docs/reference/commands.md` (lockfile
  staging correction)
- `docs/how-to/update-project-overlay.md`, `docs/how-to/diagnose-ci-failure.md`,
  `docs/reference/continuous-integration.md`, `docs/reference/generated-project.md`,
  `docs/explanation/verification-and-updates.md`, `README.md`, `docs/index.md` and
  the documentation navigation
- No new dependency, no release automation, no credential and no model access
