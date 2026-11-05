# Reproducibility and Python ownership

Why the toolchain is split between mise and uv, what that buys, and where
reproducibility stops. Design rationale lives in
[ADR 0001](decisions/0001-minimal-devkit.md); this page explains the reasoning a
user needs when the setup behaves unexpectedly.

## The failure mode this prevents

Two Python interpreters with the same version string are not the same
interpreter. A machine can hold a mise-managed CPython, a uv-managed CPython and
a distribution CPython, all reporting `3.13.18`. Code then resolves, lints and
tests against a different binary than the one that was reviewed, and the
difference surfaces later as an unreproducible bug.

The remedy is ownership, not version matching: one tool installs and selects the
interpreter, and every other tool is told to accept it.

## One owner per concern

| Scope | Owner | Why not the other |
|---|---|---|
| Language runtimes and CLI binaries | mise | uv cannot install Node.js, Codex or OpenCode, and should not try. |
| Python virtual environment and packages | uv | mise installs interpreters; it does not resolve PyPI dependency graphs. |

The split follows from the artifacts. mise deals in release archives: a Python
build, a Node.js tarball, a CLI binary. Their identity is a checksum plus, where
published, a provenance attestation. uv deals in package resolution: a graph of
wheels and sdists whose identity is a set of hashes and a resolution decision.

Mixing them would mean one lockfile claiming authority over artifacts it cannot
describe. Keeping them separate means each lockfile is complete for its own
scope:

- `mise.lock` fixes runtimes and CLIs to exact releases, with checksums and
  download URLs, plus npm sidecar locks for npm-distributed CLIs.
- `uv.lock` fixes the Python dependency graph, including development tools, to
  exact versions and hashes.

`mise install --locked` and `uv sync --locked` both refuse to re-resolve. That
refusal is the feature: an unexpected update becomes a visible failure instead of
a silent change.

## Enforcing the Python boundary

`pyproject.toml` and `mise.toml` both constrain uv, because either can be the
entry point:

- `python-downloads = "never"` and `python-preference = "only-system"` in
  `pyproject.toml` apply to every `uv` invocation in this project.
- `UV_NO_MANAGED_PYTHON = "1"` in `mise.toml` applies to anything mise runs,
  including the task definitions.

No `.python-version` file exists, so `mise.toml` is the only statement of the
required interpreter. A second version file would be a second owner, and the two
would eventually disagree.

Verification therefore compares executable paths, not version strings, and takes
the expected interpreter from mise instead of a hard-coded install directory:

```bash
mise which python
readlink -f .venv/bin/python
[ "$(readlink -f .venv/bin/python)" = "$(readlink -f "$(mise which python)")" ] \
  && echo "OK: uv uses the mise-selected interpreter"
```

The comparison must print `OK`; it fails visibly if uv ever used another
interpreter, and it assumes no fixed mise install path.

## What is reproducible, and what is not

Reproducible here means: the same reviewed commits install the same artifacts on
the same platform, and any drift is detectable before it affects a result.

Verified:

- locked installation of every runtime and CLI, with checksums checked at
  download time;
- locked Python dependency synchronization, with `uv.lock` verified against
  `pyproject.toml`;
- a documentation build that fails on broken internal links;
- verification that leaves tracked files unchanged.

Not covered, and not claimed:

- **mise itself.** It is installed manually; its version is recorded in the
  [reference](../reference/tool-versions.md), not in a lockfile.
- **Other platforms.** `mise.lock` describes `linux-x64` only. macOS and WSL2
  are untested.
- **Installer-time downloads.** npm-distributed CLIs resolve their dependencies
  through the committed sidecar locks, but mise's npm installer does not run
  package postinstall scripts by default. A package that needs one would need an
  explicit `allow_builds` option and would no longer be fully described by the
  lockfile. The pinned CLIs here install and run without that.
- **Model behavior.** Pinning a CLI version does not pin a provider's model.
- **Upstream availability.** Lockfiles pin artifacts, not the servers that
  serve them.

## Trust and review

`mise.lock` is a trust input: it names download URLs and checksums, so it is
reviewed like code. A change to a checksum that no one can explain is a reason to
stop, not to re-lock until the build passes. The same applies to a `uv.lock` diff
that adds or replaces packages unrelated to the change being reviewed.

When a pinned release is wrong, roll back with Git rather than by relaxing a
constraint; the [how-to guide](../how-to/install-toolchain.md) has the exact
commands.
