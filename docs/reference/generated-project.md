# Generated project: commands and contents

Reference for what the Copier overlay renders, which tool owns each file, and what
the generated project's tasks run. The creation procedure is the
[first-project tutorial](../tutorials/first-python-project.md).

## Template layout in this repository

```text
copier.yml                                   Copier settings and the two questions
templates/python-script-overlay/template/    the rendered overlay (nothing else is rendered)
tests/test_template.py                       generation integration test
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
| `docs/how-to/update-the-overlay.md` | how-to |
| `docs/reference/commands.md` | reference |
| `docs/explanation/ownership.md` | explanation |
| `tests/test_main.py` | smoke test: `main.py` runs and prints something |
| `.gitignore` | caches, virtual environment, secrets, generated site |
| `.copier-answers.yml` | Copier provenance: `_src_path` and `_commit` |

Never rendered: `main.py`, `pyproject.toml`, `uv.lock`, `.python-version`. uv and
the project developer own those; see
[Who owns which file](../explanation/generated-project-ownership.md).

## Tasks in the generated project

| Task | Underlying command |
|---|---|
| `mise run check` | lock check, lint, format check, type check, tests, docs |
| `mise run lock-check` | `uv lock --check` |
| `mise run lint` | `uv run --locked ruff check .` |
| `mise run format-check` | `uv run --locked ruff format --check .` |
| `mise run format` | `uv run --locked ruff format . && uv run --locked ruff check --fix .` |
| `mise run typecheck` | `uv run --locked mypy --strict main.py` |
| `mise run test` | `uv run --locked pytest` |
| `mise run docs` | `uv run --locked zensical build --strict` |
| `mise run docs-serve` | `uv run --locked zensical serve` |
| `mise run start` | `uv run --locked python main.py` |
| `mise run lock-tools` | `mise lock` |

`mise run check` runs its six checks one at a time (`[settings] jobs = 1`), so a
fresh checkout cannot race on creating `.venv`.

## Versions the overlay pins

| Tool | Version | Owner | Recorded in |
|---|---|---|---|
| Python | 3.13.18 | mise | generated `mise.toml` |
| uv | 0.13.7 | mise | generated `mise.toml` |
| Ruff | 0.17.3 | uv | generated `pyproject.toml`, `uv.lock` |
| mypy | 2.4.1 | uv | generated `pyproject.toml`, `uv.lock` |
| pytest | 9.2.0 | uv | generated `pyproject.toml`, `uv.lock` |
| Zensical | 0.0.74 | uv | generated `pyproject.toml`, `uv.lock` |
| Copier (applies the overlay) | 9.19.1 | uv | this repository's `pyproject.toml` |

The four Python tools are installed in the generated project with `uv add --dev`,
using those exact versions. The overlay renders no dependency list, so the versions
exist once, in the project's own uv-owned manifest.

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

The test creates a project with the real `mise`, `uv`, `git` and Copier
executables — no mocks — in a temporary directory whose name contains a space. It
asserts:

1. the project is created, runs, passes its smoke test and passes its own
   `mise run check`;
2. `main.py` and `pyproject.toml` are byte-identical to the uv output after the
   overlay is applied, and no template file could render them;
3. the exact dependency versions are recorded in `pyproject.toml` and `uv.lock`;
4. native `mise lock` writes the project's own `mise.lock`; it records exactly the
   Python and uv versions pinned by the rendered `mise.toml`, with a checksum and
   a download URL for `linux-x64`, and it is not a copy of this repository's
   `mise.lock`;
5. `mise install --locked` installs that lockfile into a throwaway mise
   installation whose data, cache and state directories live inside the fixture,
   and `mise run check` passes with those freshly installed tools;
6. provenance is recorded, including a tag from a temporary tagged repository;
7. the project is independent: its own `.venv`, its own `uv.lock` and
   `mise.lock`, no `.python-version`, no workspace membership, no agent
   configuration;
8. a deliberately broken test and a lint violation each make `mise run check` fail,
   and the fixture is restored afterwards;
9. Copier answers containing double quotes, backslashes, Unicode and newlines
   render a `zensical.toml` that `tomllib` parses back to the original answers, so
   no punctuation has to be forbidden in a project name or description;
10. the devkit working tree is unchanged by the run.

The overlay never copies this repository's `mise.lock` into a project. A lock
describes the platform it was created on, so the generated project runs
`mise lock` once and commits the result; the split between the two lockfiles is
[Reproducibility](../explanation/reproducibility.md).

`test-template` is not part of `mise run check`: it installs packages from the
package index, downloads the locked toolchain archives and is the slower
integration gate. CI is expected to run both.
