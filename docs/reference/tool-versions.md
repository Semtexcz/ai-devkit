# Tool ownership and pinned versions

Reference for what each tool owns, the exact versions this repository has been
verified with, and the files that record them.

## Ownership

Each concern has one owner. Overlap is a defect, not a convenience.

| Concern | Owner | Recorded in |
|---|---|---|
| Runtimes and CLI versions | mise | `mise.toml`, `mise.lock`, `.mise/locks/` |
| Python interpreter installation and selection | mise | `mise.toml` (`python`), installed under the mise data directory |
| Python virtual environment and dependencies | uv | `pyproject.toml`, `uv.lock`, `.venv/` (ignored) |
| Documentation site build and link validation | Zensical | `zensical.toml` |
| Documentation structure | Diátaxis | `docs/tutorials`, `docs/how-to`, `docs/reference`, `docs/explanation` |
| Development tasks | mise tasks | `[tasks]` in `mise.toml` |

## Pinned versions

Verified on Linux x86-64 with `mise run versions`.

| Tool | Version | mise backend or source | Owner |
|---|---|---|---|
| mise | 2026.11.1 | official release archive, installed manually | host |
| Python | 3.13.18 | `core:python` | mise |
| Node.js | 24.22.2 | `core:node` | mise |
| uv | 0.13.7 | `aqua:astral-sh/uv` | mise |
| OpenSpec | 1.16.0 | `npm:@fission-ai/openspec` | mise |
| OpenCode | 1.19.5 | `github:anomalyco/opencode` | mise |
| OpenAI Codex CLI | 0.163.0 | `aqua:openai/codex` | mise |
| Copier | 9.19.1 | PyPI via `pyproject.toml` | uv |
| pytest | 9.2.0 | PyPI via `pyproject.toml` | uv |
| Ruff | 0.17.3 | PyPI via `pyproject.toml` | uv |
| mypy | 2.4.1 | PyPI via `pyproject.toml` | uv |
| Zensical | 0.0.74 | PyPI via `pyproject.toml` | uv |

`mise run versions` prints this tuple, including the tool-owned version output
formats (for example `codex-cli 0.163.0` and a bare `0.0.74` from Zensical).

### Why these distributions

- **uv** is installed from its official GitHub releases through mise's aqua
  backend rather than from PyPI, so `mise.lock` records a checksum together with
  GitHub artifact attestations.
- **Codex CLI** comes from the official `openai/codex` GitHub release through
  the aqua backend. The npm package `@openai/codex` is also official; the release
  archive is preferred here because mise verifies its checksum.
- **OpenSpec** is a Node.js CLI published as `@fission-ai/openspec`. mise has no
  registry entry for it, so the npm backend is declared with that package name,
  and its dependency graph is locked in a sidecar under `.mise/locks/`.
- **OpenCode** is pinned to the 1.x line (`1.19.5`), which is the line the
  approved plan targets for the DeepSeek integration, and is installed from the
  vendor's GitHub releases, as their installation documentation recommends for
  mise. OpenCode 2 is a separate distribution and is not selected here.

## Lockfiles and sidecars

| File | Contents | Tracked |
|---|---|---|
| `mise.lock` | resolved versions, checksums, download URLs, provenance for every mise tool | yes |
| `.mise/locks/npm-fission-ai-openspec/1.16.0/` | npm dependency lock (`aube-lock.yaml`, `package.json`) for the OpenSpec CLI | yes |
| `uv.lock` | complete Python dependency graph with hashes | yes |
| `site/`, `.venv/`, caches | generated output and local environments | no |

`mise.lock` covers the `linux-x64` platform only, as declared by
`lockfile_platforms` in `mise.toml`. mise itself is installed by hand, so the
mise version is recorded in this table rather than in the lockfile.

## Python interpreter

mise owns Python; uv must use the interpreter mise selected.

| Guarantee | Mechanism |
|---|---|
| mise selects the interpreter | `python = "3.13.18"` in `mise.toml` |
| uv cannot download another one | `python-downloads = "never"` in `pyproject.toml`, `UV_NO_MANAGED_PYTHON=1` in `mise.toml` |
| uv cannot prefer a managed one | `python-preference = "only-system"` in `pyproject.toml` |
| No second version file exists | there is no `.python-version`; `mise.toml` is authoritative |

Verify the identity of the interpreter rather than the version string. Compare
the interpreter mise selects with the one the environment uses, so the check
does not depend on mise's installation directory:

```bash
mise which python                                  # mise-selected interpreter
readlink -f .venv/bin/python                       # interpreter the venv uses
[ "$(readlink -f .venv/bin/python)" = "$(readlink -f "$(mise which python)")" ] \
  && echo "OK: uv uses the mise-selected interpreter"
mise exec -- uv run python -c 'import sys; print(sys.executable)'
```

The comparison must print `OK`; `mise which` reflects the active mise data
directory, so no fixed install path is assumed.

## Tasks

| Command | Runs |
|---|---|
| `mise run docs` | `uv run --locked zensical build --strict` |
| `mise run docs-serve` | `uv run --locked zensical serve` |
| `mise run check` | `mise run lock-check`, `mise run examples-check`, then `mise run docs` |
| `mise run lock-check` | `uv lock --check` |
| `mise run examples-check` | parses the JSON and TOML agent configuration examples |
| `mise run versions` | prints every pinned version |

`check` deliberately contains only the checks that exist today. Ruff, mypy,
pytest and OpenSpec checks arrive with the application and OpenSpec tasks.
