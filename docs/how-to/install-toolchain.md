# Install the development toolchain

How to install, verify, update and roll back the toolchain declared in
`mise.toml`. For a guided first run, use the
[tutorial](../tutorials/getting-started.md) instead.

## Prerequisites

- Linux x86-64 (only verified platform) with Git, `curl`, `tar` and CA
  certificates.
- mise 2026.11.1 or newer, installed in your user account. `mise.toml` declares
  `min_version = "2026.11.1"`.
- No administrator privileges, no global shell configuration changes, and no
  credentials: installing and checking the toolchain needs neither.

## Install the toolchain

```bash
mise trust                      # once per clone; review mise.toml first
mise install --locked           # runtimes, CLIs, checksum-verified
mise exec -- uv sync --locked   # Python development tools from uv.lock
```

`mise install --locked` refuses to resolve anything that `mise.lock` does not
record, which is the point: the installed tuple is the reviewed one.

Commit `mise.lock`, the npm sidecar locks under `.mise/locks/` and `uv.lock`.
Without the sidecars, the transitive dependency graph of the npm-installed CLIs
would be re-resolved on every machine.

## Verify the installation

```bash
mise run versions
```

That task prints mise, Python, Node.js, uv, OpenSpec, OpenCode, Codex and each
Python development tool. Compare the output with the pinned versions in the
[reference](../reference/tool-versions.md).

Also confirm that uv did not acquire its own interpreter. Ask mise which
interpreter it selects, then compare it with the one the environment uses; the
comparison assumes no fixed mise installation directory:

```bash
mise which python
readlink -f .venv/bin/python
[ "$(readlink -f .venv/bin/python)" = "$(readlink -f "$(mise which python)")" ] \
  && echo "OK: uv uses the mise-selected interpreter"
```

The comparison must print `OK`. `mise which` reports the path inside whatever
data directory the current mise uses, so the check assumes no fixed location —
it holds when `MISE_DATA_DIR` is set, as long as the toolchain is installed in
that data directory.

Each tool can also be invoked directly, which is useful when a global install
of the same name exists on your `PATH`:

```bash
mise exec -- uv --version       # the pinned uv, not any other uv on PATH
for tool in python node uv openspec opencode codex; do mise which "$tool"; done
```

## Update a tool version

Update one tool at a time so that a failure has a single candidate cause.

1. Change the version in `mise.toml`.
2. Regenerate the lockfile and install it:

   ```bash
   mise lock
   mise install --locked
   ```

3. Review the lockfile diff. Expected changes are the version, the checksum and
   the download URL of that tool, plus sidecar changes under `.mise/locks/` for
   npm tools.
4. Re-run the checks:

   ```bash
   mise exec -- uv sync --locked
   mise run check
   ```

Python development tools live in `pyproject.toml` and are pinned by `uv.lock`
(versions below are examples; replace them with the release you reviewed):

```bash
mise exec -- uv add --dev ruff~=0.18.0   # changes pyproject.toml and uv.lock
mise exec -- uv lock --upgrade-package mypy
mise run check
```

## Roll back to a known working configuration

Lockfiles are committed, so rollback is a Git operation followed by a
re-install. Two situations need different commands: discarding edits you have
not committed yet, and returning to a version that was committed earlier.

Inspect the state first, so you know which situation applies:

```bash
git status --short
git diff -- mise.toml mise.lock .mise/locks pyproject.toml uv.lock
```

### Discard uncommitted edits

This is not a rollback to an earlier release; it throws the edits away and
returns the files to the last commit, whether the edits were staged or not.
They are unrecoverable afterwards, so review the diff above first.

```bash
git restore --source=HEAD --staged --worktree -- \
  mise.toml mise.lock .mise/locks pyproject.toml uv.lock
```

Files Git does not track — for example a sidecar directory you generated but
never added — are left alone; `git status --short` lists them with `??`.

### Restore a previously committed, known-good version

Find the commit whose toolchain you want back, then read those paths out of it.
The contents land in your working tree as uncommitted changes; nothing is
rewritten in history and your current commit stays intact.

```bash
git log --oneline -- mise.toml mise.lock
COMMIT=abc1234          # replace with the commit, tag or branch you chose
git restore --source="$COMMIT" --worktree -- \
  mise.toml mise.lock .mise/locks pyproject.toml uv.lock
git diff --stat
```

Review `git diff` and commit the result once you accept it, so the next
rollback starts from a known point.

`git restore` only touches the paths you name. A path that is tracked but does
not exist in that commit is removed from the working tree, so `.mise/locks/`
cannot end up holding two sidecar versions. A path you never committed stays
untracked and therefore remains; `git status --short` lists it with `??`, and
you should remove it before re-installing so the tree holds one toolchain
version.

### Re-install and verify either way

```bash
mise install --locked
mise exec -- uv sync --locked
mise run check
```

Then confirm that verification changed no tracked file, other than the rollback
itself:

```bash
git status --short
```

## Troubleshoot

| Symptom | Cause and fix |
|---|---|
| `Config files ... are not trusted` | Run `mise trust` in the repository root after reviewing `mise.toml`. |
| `... is not in the lockfile` | `mise.toml` was edited without `mise lock`. Run `mise lock`, review the diff, then `mise install --locked`. |
| Checksum mismatch | The upstream artifact changed. Do not delete checksums; investigate the release first, then refresh only that entry with `mise lock <tool>`. |
| uv selects an unexpected interpreter | uv must run under mise: use `mise exec -- uv ...` or `mise run ...`. `pyproject.toml` already sets `python-preference = "only-system"` and `python-downloads = "never"`. |
| `uv: command not found` | The mise environment is not active. Use `mise exec -- uv ...`, or reinstall the toolchain with `mise install --locked`. Do not change global shell configuration from a project. |

## Platform limitations

- `mise.lock` records artifacts for `linux-x64` only, as declared by
  `lockfile_platforms` in `mise.toml`. On another platform, add it there and
  re-run `mise lock`; the resulting entry is untested until someone runs it.
- macOS and WSL2 are not verified. Clean-machine evidence for Linux x86-64 is
  recorded in the
  [v0.1.0 acceptance report](../releases/v0.1.0-acceptance-report.md).
- mise itself is installed manually and is not covered by `mise.lock`; the
  tested version is recorded in the reference.
