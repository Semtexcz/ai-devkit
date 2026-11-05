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

Also confirm that uv did not acquire its own interpreter:

```bash
readlink -f .venv/bin/python    # must point into ~/.local/share/mise/installs/python/
```

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
re-install:

```bash
git checkout -- mise.toml mise.lock .mise/locks pyproject.toml uv.lock
mise install --locked
mise exec -- uv sync --locked
mise run check
```

Then confirm that verification changed no tracked file:

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
- macOS and WSL2 are not verified. Task 7 of the plan owns clean-machine
  evidence.
- mise itself is installed manually and is not covered by `mise.lock`; the
  tested version is recorded in the reference.
