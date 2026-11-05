# Getting started

This tutorial takes you from a fresh clone to a verified documentation build.
It assumes Linux on x86-64 and takes about ten minutes, most of it downloads.

You will clone the repository, install a pinned version of mise into your user
account, let mise install the exact toolchain recorded in `mise.lock`, create
the Python environment from `uv.lock`, and finish by building the documentation.

## Before you begin

You need:

- Linux x86-64. This is the only verified platform.
- Git, to clone the repository.
- `curl`, `tar`, `sha256sum` from coreutils, and CA certificates, to download,
  verify and unpack the tools.
- A user account that can write to `~/.local`. No `sudo` is required at any
  point.

Check the basics:

```bash
git --version
curl --version
tar --version
sha256sum --version
```

mise is not assumed to be installed already: Step 1 clones the repository and
Step 2 installs mise.

## Step 1: Clone the repository

```bash
git clone https://github.com/Semtexcz/ai-devkit.git
cd ai-devkit
```

Every command in this tutorial runs from the repository root, which is the
directory that contains `mise.toml`. If you get lost, check with `pwd` and
return with `cd` to the directory you cloned into.

## Step 2: Install mise

The toolchain is defined by mise, so mise itself is installed first. Use the
official release archive for the pinned release instead of a moving "latest"
installer, and check the published checksum before running the binary.

The block below is ordered so that a failure cannot be followed by an install.
The installation is a single subshell that stops at its first error, and its
exit status decides whether anything after it runs: the archive is unpacked in a
temporary directory and moved into place only after the checksum and the
unpacked binary check out, an `EXIT` trap removes the temporary directory
whether the attempt succeeds or fails, and an existing installation is refused
rather than overwritten. The subshell also keeps your shell in the repository
root, and the last lines export `PATH` so every later command finds the new
binary.

```bash
MISE_VERSION=2026.11.1
mise_root="$HOME/.local/opt/mise"
mise_bin="$HOME/.local/bin/mise"
mkdir -p "$HOME/.local/opt" "$HOME/.local/bin"

(
  set -eu                        # stop at the first failing step
  for path in "$mise_root" "$mise_bin"; do
    if [ -e "$path" ] || [ -L "$path" ]; then
      echo "ERROR: $path already exists; refusing to overwrite it" >&2
      exit 1
    fi
  done
  work="$(mktemp -d)"
  trap 'rm -rf "$work"' EXIT     # cleanup after success and after failure
  cd "$work"
  base="https://github.com/jdx/mise/releases/download/v$MISE_VERSION"
  archive="mise-v$MISE_VERSION-linux-x64.tar.gz"
  curl -fsSLO "$base/$archive"
  curl -fsSLO "$base/SHASUMS256.txt"
  grep -F "$archive" SHASUMS256.txt > expected.sha256
  sha256sum -c expected.sha256   # a mismatch stops here, before extraction
  tar -xzf "$archive"            # unpacks into the temporary directory
  test -x "$work/mise/bin/mise"  # the archive must contain the binary
  mv "$work/mise" "$mise_root"   # first step that touches the install path
  ln -s ../opt/mise/bin/mise "$mise_bin"
)
mise_status=$?                   # 0 only if every step above succeeded

if [ "$mise_status" -eq 0 ]; then
  export PATH="$HOME/.local/bin:$PATH"
  hash -r                        # forget a previously resolved mise
  pwd                            # must print the repository root
  command -v mise                # must print $HOME/.local/bin/mise
  mise --version                 # must print 2026.11.1
else
  echo "ERROR: mise was not installed; fix the error above." >&2
  echo "If $mise_root exists, remove it before retrying." >&2
fi
```

The checksum line must end with `OK`, `pwd` must still print the repository
root, `command -v mise` must print `$HOME/.local/bin/mise`, and
`mise --version` must print `2026.11.1`.

If the block prints `ERROR: mise was not installed`, nothing was installed: the
subshell stopped at the failing step, the temporary directory was removed, and
neither install path was created. Fix the reported cause — a failed download, a
checksum mismatch or an unusable archive — and run the block again.

`ERROR: ... already exists` appears just above that line when an earlier
installation was found; it was left untouched. Remove `~/.local/opt/mise` and
`~/.local/bin/mise` yourself only if you do intend to replace them.

The `export PATH` above applies to the current shell. A new shell needs
`~/.local/bin` on its `PATH` from your shell profile.

## Step 3: Review and trust the project configuration

mise refuses to read a project configuration it has not been told to trust.
Read `mise.toml` first — it is short, and it names every tool and backend — then
trust it:

```bash
mise trust
mise config ls
```

`mise config ls` lists the tools the configuration declares. Trust is recorded
in your own mise state, so no global shell configuration changes.

## Step 4: Install the locked toolchain

```bash
mise install --locked
```

`--locked` installs only the versions recorded in `mise.lock` and verifies the
recorded checksums. If mise reports a tool that is "not in the lockfile", the
configuration and the lockfile disagree; see the
[how-to guide](../how-to/install-toolchain.md).

Confirm what you have:

```bash
mise exec -- bash -c \
  'python --version; node --version; uv --version; openspec version; opencode --version; codex --version'
```

Expect Python 3.13.18, Node.js v24.22.2, uv 0.13.7, OpenSpec 1.16.0,
OpenCode 1.19.5 and codex-cli 0.163.0.

## Step 5: Create the Python environment

```bash
mise exec -- uv sync --locked
```

`uv sync --locked` installs the development tools recorded in `uv.lock` into
`.venv`. It does not install a Python interpreter: mise provides it and uv is
configured to use only a system interpreter.

Check that the environment uses the interpreter mise selected. Ask mise for the
interpreter it selects, resolve both sides to real paths, and compare them —
this makes no assumption about where mise keeps its installations:

```bash
mise which python
readlink -f .venv/bin/python
[ "$(readlink -f .venv/bin/python)" = "$(readlink -f "$(mise which python)")" ] \
  && echo "OK: the virtual environment uses the mise-selected interpreter"
```

The comparison must print `OK`. The two paths differ only in how they are
reached: `.venv/bin/python` is a link into the interpreter that `mise which`
reports. Because the expected value comes from mise rather than from a
documented install location, the check also holds when mise installs its tools
somewhere other than the default data directory.

`uv run` reports the environment's own path instead, which is expected:

```bash
mise exec -- uv run python -c 'import sys; print(sys.executable)'
```

## Step 6: Build the documentation

```bash
mise run docs
```

The site is written to `site/`, which is ignored by Git. The build runs in
strict mode: a broken internal link or anchor aborts it with a nonzero exit
code.

Preview it locally with live reload:

```bash
mise run docs-serve   # http://localhost:8000
```

## Step 7: Run the full check

```bash
mise run check
```

At this stage `check` verifies that `uv.lock` matches `pyproject.toml` and that
the documentation builds strictly. Application linting, type checking, tests
and OpenSpec validation arrive with later tasks.

You now have a reproducible maintainer environment. To change versions safely,
read [Install the development toolchain](../how-to/install-toolchain.md); to
understand why the toolchain is split between mise and uv, read
[Reproducibility and Python ownership](../explanation/reproducibility.md).
