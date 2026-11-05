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
- `curl`, `tar` and CA certificates, to download and unpack the tools.
- A user account that can write to `~/.local`. No `sudo` is required at any
  point.

Check the basics:

```bash
git --version
curl --version
tar --version
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

The download runs in a disposable directory inside a subshell, so your shell
stays in the repository root for the updated environment and for every later
step.

```bash
MISE_VERSION=2026.11.1
mkdir -p ~/.local/opt ~/.local/bin
work="$(mktemp -d)"
(
  cd "$work" || exit 1
  curl -fsSLO "https://github.com/jdx/mise/releases/download/v$MISE_VERSION/mise-v$MISE_VERSION-linux-x64.tar.gz"
  curl -fsSLO "https://github.com/jdx/mise/releases/download/v$MISE_VERSION/SHASUMS256.txt"
  sha256sum -c <(grep "mise-v$MISE_VERSION-linux-x64.tar.gz" SHASUMS256.txt)
  tar -xzf "mise-v$MISE_VERSION-linux-x64.tar.gz" -C ~/.local/opt
)
rm -rf "$work"
ln -sfn ../opt/mise/bin/mise ~/.local/bin/mise
pwd          # must print the repository root
mise --version
```

The checksum line must end with `OK`, `pwd` must still print the repository
root, and `mise --version` must print `2026.11.1`. `~/.local/bin` already needs
to be on your `PATH`; for this session, prefix commands with
`PATH="$HOME/.local/bin:$PATH"` if it is not. If mise is still not found after
that, open a new shell before continuing.

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
