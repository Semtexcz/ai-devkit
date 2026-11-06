# Generated project: commands and contents

Reference for what the Copier overlay renders, which tool owns each file, and what
the generated project's tasks run. The creation procedure is the
[first-project tutorial](../tutorials/first-python-project.md).

## Template layout in this repository

```text
copier.yml                                   Copier settings and the two questions
templates/python-script-overlay/template/    the rendered overlay (nothing else is rendered)
tests/                                       generation, update lifecycle and CI workflow tests
.github/workflows/verify.yml                 read-only verification on GitHub Actions
```

`copier.yml` sets `_subdirectory` to the template directory, so the rest of the
devkit — its own documentation, toolchain configuration and tests — is never
copied into a project. Keeping the template source at the repository root is what
lets Copier record a version: it treats the repository as a template source, checks
out `--vcs-ref`, and stores `_commit`.

## Files the overlay renders

| Path | Purpose |
|---|---|
| `AGENTS.md` | engineering rules: reuse-first, small changes, documentation, security, Definition of Done |
| `mise.toml` | pinned Python and uv, tasks, single-owner environment |
| `ruff.toml` | lint and format policy only |
| `mypy.ini` | `strict = True` type-checking policy only |
| `pytest.ini` | test discovery only |
| `zensical.toml` | documentation site configuration |
| `README.md` | project contract and quick start |
| `docs/index.md` | documentation entry point |
| `docs/tutorials/run-the-script.md` | tutorial |
| `docs/how-to/add-a-dependency.md` | how-to |
| `docs/how-to/use-openspec.md` | how-to: initialize OpenSpec, propose, validate, archive |
| `docs/how-to/update-the-overlay.md` | how-to |
| `docs/reference/commands.md` | reference |
| `docs/explanation/ownership.md` | explanation |
| `tests/test_main.py` | smoke test: `main.py` runs and prints something |
| `.gitignore` | caches, virtual environment, secrets, generated site |
| `.copier-answers.yml` | Copier provenance: `_src_path` and `_commit` |

Never rendered: `main.py`, `pyproject.toml`, `uv.lock`, `.python-version`. uv and
the project developer own those; see
[Who owns which file](../explanation/generated-project-ownership.md).

Also never rendered: `openspec/`, `.opencode/` and `.agents/`. Those are created by
`openspec init` inside the project, and refreshed by `openspec update`. A copy in the
overlay would be a second owner that drifts from the pinned CLI, so the integration
test asserts that no template path is one of them.

## Tasks in the generated project

| Task | Underlying command |
|---|---|
| `mise run check` | lock check, lint, format check, type check, tests, docs, specs |
| `mise run lock-check` | `uv lock --check` |
| `mise run lint` | `uv run --locked ruff check .` |
| `mise run format-check` | `uv run --locked ruff format --check .` |
| `mise run format` | `uv run --locked ruff format . && uv run --locked ruff check --fix .` |
| `mise run typecheck` | `uv run --locked mypy --strict main.py` |
| `mise run test` | `uv run --locked pytest` |
| `mise run docs` | `uv run --locked zensical build --strict` |
| `mise run docs-serve` | `uv run --locked zensical serve` |
| `mise run spec-check` | `openspec validate --all --strict --no-interactive` |
| `mise run start` | `uv run --locked python main.py` |
| `mise run lock-tools` | `mise lock` |

`mise run check` runs its seven checks one at a time (`[settings] jobs = 1`), so a
fresh checkout cannot race on creating `.venv`. The OpenSpec check requires the
project's one-time `openspec init`; without an `openspec/` root it fails instead of
skipping.

## Versions the overlay pins

| Tool | Version | Owner | Recorded in |
|---|---|---|---|
| Python | 3.13.18 | mise | generated `mise.toml` |
| uv | 0.13.7 | mise | generated `mise.toml` |
| Node.js | 24.22.2 | mise | generated `mise.toml` |
| OpenSpec | 1.16.0 | mise | generated `mise.toml` |
| Ruff | 0.17.3 | uv | generated `pyproject.toml`, `uv.lock` |
| mypy | 2.4.1 | uv | generated `pyproject.toml`, `uv.lock` |
| pytest | 9.2.0 | uv | generated `pyproject.toml`, `uv.lock` |
| Zensical | 0.0.74 | uv | generated `pyproject.toml`, `uv.lock` |
| Copier (applies the overlay) | 9.19.1 | uv | this repository's `pyproject.toml` |

The four Python tools are installed in the generated project with `uv add --dev`,
using those exact versions. The overlay renders no dependency list, so the versions
exist once, in the project's own uv-owned manifest.

Node.js is pinned because OpenSpec is a Node.js CLI. `mise lock` records Python, uv
and Node.js with a per-platform checksum and URL, and OpenSpec through an npm
dependency sidecar under `.mise/locks/`, so the generated project can run OpenSpec
without a global installation or a copy from this repository.

## Provenance

`.copier-answers.yml` in a generated project looks like this:

```yaml
_commit: v0.1.0
_src_path: gh:Semtexcz/ai-devkit
project_description: A small Python script project.
project_name: my script
```

- `_src_path` is the template source exactly as it was passed to `copier copy`.
- `_commit` is the template version: a release tag, or a commit description for
  `--vcs-ref HEAD` (a synthetic commit when the source tree has uncommitted
  changes).

`_commit` must exist in the template repository for `copier update` to diff against
it. A project copied from an uncommitted working tree records a synthetic commit and
fails to update with `ValueError: Unknown revision`; use a tagged release, or a clean
commit, for projects that should receive updates.

Commit the file. It is the only input `copier update` needs, and editing it by hand
breaks the update path. The update procedure is
[Update a project's overlay](../how-to/update-project-overlay.md).

## Verifying the overlay in this repository

```bash
mise run test-template
```

The test creates a project with the real `mise`, `uv`, `git`, Copier and OpenSpec
executables — no mocks — in a temporary directory whose name contains a space. It
asserts:

1. the project is created, runs, passes its smoke test and passes its own
   `mise run check`;
2. `main.py` and `pyproject.toml` are byte-identical to the uv output after the
   overlay is applied, and no template file could render them or copy an agent
   integration;
3. the exact dependency versions are recorded in `pyproject.toml` and `uv.lock`;
4. native `mise lock` writes the project's own `mise.lock`; it records exactly the
   Python, uv, Node.js and OpenSpec versions pinned by the rendered `mise.toml` — with
   a checksum and a download URL for the archive tools and an npm sidecar with a
   digest for OpenSpec — and it is not a copy of this repository's `mise.lock`;
5. `mise install --locked` installs that lockfile into a throwaway mise installation
   whose data, cache, state and `XDG_CONFIG_HOME` live inside the fixture, and
   `mise run check` passes with those freshly installed tools;
6. `.venv` is recreated with that isolated toolchain, and the interpreter identity is
   verified through `sys.base_prefix` and `readlink -f` rather than a version string;
7. `openspec init --tools opencode,codex --profile core`, run by the project's own
   pinned CLI, produces `openspec/`, `.opencode/commands/` and `.agents/skills/`, and
   the project's `mise run check` validates specifications with the native command;
8. provenance is recorded, including a tag from a temporary tagged repository;
9. the project is independent: its own `.venv`, its own `uv.lock` and `mise.lock`, no
   `.python-version`, no workspace membership, no agent credentials or model settings;
10. each of six deliberate defects fails `mise run check`, and each is reported by
    the task that owns the checker rather than by a neighbouring one: a Ruff lint
    violation (`mise run lint`), a Ruff formatting violation
    (`mise run format-check`), a `mypy --strict` violation (`mise run typecheck`), a
    failing test (`mise run test`), a broken internal documentation link
    (`mise run docs`) and an invalid OpenSpec specification (`mise run spec-check`).
    The fixture is restored after every case and the restored project passes again;
11. the worked example in `examples/openspec-change/` runs the full lifecycle in the
    project — propose, validate, implement, test, document, validate, `mise run check`,
    mark tasks complete, archive — and the archived project still passes its check;
12. Copier answers containing double quotes, backslashes, Unicode and newlines render
    a `zensical.toml` that `tomllib` parses back to the original answers, so no
    punctuation has to be forbidden in a project name or description;
13. native `copier update` between two temporary tagged revisions (`v0.1.0` and
    `v0.2.0`) preserves an edited `main.py`, a project regression test,
    `pyproject.toml` and `uv.lock` byte for byte, and the updated project still passes
    its check;
14. the same update preserves a project-owned documentation page, its link from the
    documentation entry point, and the project's own edit to an overlay-owned page
    the template did not change;
15. a project edit to the same region of `AGENTS.md` that the newer revision changes
    produces inline conflict markers, unmerged Git stages and both sides' text; after
    a hand resolution that keeps both, the project passes its check and the update
    commits as one change;
16. the update advances `_commit` in `.copier-answers.yml`, keeps `_src_path` pointing
    at the template repository, leaves the project's answers unchanged, rewrites only
    the files the template changed, and is reported as up to date by
    `copier check-update`;
17. the devkit working tree is unchanged by the run.

The update scenarios run in copies of one prepared project: creating and locking a
project is the expensive part, while each scenario needs its own committed tree.
The slow per-scenario step is `uv sync --locked`, which rebuilds `.venv` from the
copy's own lockfile.

The never-rendered rule is what makes items 13–16 possible: an update cannot
overwrite a file the template never produces. The overlay never copies this
repository's `mise.lock` into a project either: a lock describes the platform it
was created on, so the generated project runs `mise lock` once and commits the
result. The split between the two lockfiles is
[Reproducibility](../explanation/reproducibility.md).

`test-template` is not part of `mise run check`: it installs packages from the
package index, downloads the locked toolchain archives and is the slower
integration gate. CI runs both; see
[Continuous integration](continuous-integration.md).
