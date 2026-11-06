# Tasks

## 1. Hosted verification

- [x] 1.1 Add a read-only GitHub Actions workflow for pushes and pull requests to `main`
- [x] 1.2 Pin the workflow's actions to full commit identifiers and the mise version explicitly
- [x] 1.3 Install the locked toolchain, then run `mise run versions`, `mise run check` and `mise run test-template`
- [x] 1.4 Fail the job when verification changes a tracked file
- [x] 1.5 Reject write permissions, unpinned actions, secrets and privileged pull-request execution in a test

## 2. Update lifecycle

- [x] 2.1 Build a temporary template repository with tagged `v0.1.0` and `v0.2.0` revisions and a controlled overlay change
- [x] 2.2 Prove that a project's entry point, regression test, `pyproject.toml` and `uv.lock` survive an update
- [x] 2.3 Prove that a project-owned documentation page and a local edit to an overlay-owned page survive an update
- [x] 2.4 Prove that a same-region edit to `AGENTS.md` produces a visible, resolvable conflict and that neither side is dropped
- [x] 2.5 Prove that provenance advances, the source path is preserved and no unrelated file is rewritten

## 3. Failure detection

- [x] 3.1 Prove a Ruff lint violation, a Ruff formatting violation, a mypy violation and a failing test each fail the check for their own reason
- [x] 3.2 Prove a broken internal documentation link fails the strict documentation build and the check
- [x] 3.3 Keep the invalid-specification case and prove the restored project passes again
- [x] 3.4 Share the expensive project setup between the test modules without sharing a mutable working tree

## 4. Documentation

- [x] 4.1 Document how CI works and how to diagnose a failed job
- [x] 4.2 Document the native update procedure and how to resolve a conflicting update
- [x] 4.3 Record the CI triggers, commands, test coverage, update guarantees and ownership boundaries in the reference
- [x] 4.4 Explain why CI reuses the mise tasks, why updates are reviewed changes and why project-owned files stay independent
- [x] 4.5 Correct the overlay's lockfile instructions to stage the npm sidecar locks too
