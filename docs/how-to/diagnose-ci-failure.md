# Diagnose a failed CI job

How to find out what hosted verification reported, reproduce it locally, and decide
whether the failure is in the change or in the environment. For what the pipeline
runs and why, see the
[continuous integration reference](../reference/continuous-integration.md).

## 1. Find the failing step

Open the failed run, then its `verify (ubuntu-24.04)` job. The step names are the
documented command sequence, so the failing step tells you which layer broke:

| Failing step | Read it as |
|---|---|
| `Install the locked toolchain` | `mise.lock`, `.mise/locks/` or `uv.lock` does not match its manifest |
| `Print the installed versions` | a tool is missing or reports an unexpected version |
| `Run the repository checks` | `mise run check` failed: lock, agent examples, specs or docs |
| `Run the generation and update integration test` | `mise run test-template` failed: generation, ownership, update lifecycle or failure detection |
| `Confirm verification changed no tracked file` | a check wrote a tracked file |

## 2. Reproduce it locally

Clone the same commit and run the same commands from the repository root:

```bash
mise trust
mise install --locked
mise exec -- uv sync --locked
mise run versions
mise run check
mise run test-template
git status --short
```

A local reproduction that passes while the job fails almost always means an
environment difference, not a code difference. Check, in this order:

1. **The mise version.** `mise --version` must print `2026.11.1`. An older mise
   cannot read the lockfile the workflow installs.
2. **The interpreter.** `mise which python` must point inside the mise data
   directory, and `readlink -f .venv/bin/python` must resolve to the same file.
   A uv-managed interpreter means `UV_NO_MANAGED_PYTHON=1` was not in effect.
3. **Leftover local state.** A green local run that started from an existing
   `.venv` proves less than a fresh one:

   ```bash
   rm -rf .venv site
   mise exec -- uv sync --locked
   mise run check
   ```

4. **The package index.** `mise run test-template` installs a generated project's
   dependencies. A proxy, mirror or offline machine changes its result, while
   `mise run check` stays green.

## 3. Read the integration test's own message

`mise run test-template` fails with the captured output of the command that broke,
including a command line, exit code and both streams. Two patterns cover most
failures:

- `command failed with exit code N: ...` — a tool rejected the repository. The
  command line names the fixture and the tool.
- `Copier did not report the conflict` — the update lifecycle test expected inline
  conflict markers and found none. That means the pinned Copier changed how it
  reports conflicts, which is a change in behavior this repository must review,
  not a flake.

## 4. Confirm the failure is in the intended checker

A failing check is not proof that the intended checker works: a broken formatting
test that also breaks linting proves nothing about formatting. The negative cases in
`tests/test_template.py` therefore assert twice — once on the task that owns the
checker, once on `mise run check`:

```bash
cd <a generated project>
mise run lint          # or format-check, typecheck, test, docs, spec-check
mise run check
```

If the owning task passes but `mise run check` fails, the defect is in a different
checker; find the step whose output mentions the file you changed.

## 5. Reproduce a CI-only dependency problem

If the failure mentions a version, a checksum or a missing artifact, do not edit the
lockfile by hand. Regenerate it with its owner and review the diff:

```bash
mise lock                 # tool versions, checksums, .mise/locks/ sidecars
mise install --locked
mise exec -- uv lock      # Python dependency graph
mise run check
```

## 6. Report the result honestly

A local run does not verify hosted CI. If GitHub has not executed the workflow for
the change, report hosted verification as **pending**, not passed — the two are
separate acceptance results.

## When the failure is the workflow itself

If a step name, permission, pinned commit or timeout is wrong, the fix belongs in
`.github/workflows/verify.yml`, and `tests/test_ci_workflow.py` guards the
properties that matter: pinning, read-only permissions, the command sequence and
the absence of secrets and publishing steps.
