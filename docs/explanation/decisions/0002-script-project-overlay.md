# 0002 — Script project overlay: policy only, native provenance

- **Status:** Accepted
- **Date:** 2026-11-05

## Context

[ADR 0001](0001-minimal-devkit.md) fixes the ownership model: native `uv init`
creates the application, uv owns the Python environment and lockfiles, mise owns
runtimes and tasks, and Copier provides a thin standards overlay. Delivering the
first project (v0.1 plan, Task 4) forced concrete decisions about what the overlay
may render, where the template source lives, and how a project can later take an
overlay update.

The constraints: no custom generator CLI, no second dependency manager, no
duplicated configuration ownership, and no template that can overwrite application
code or a dependency manifest.

## Decision

1. **The overlay renders policy, never resolution.** It renders rules
   (`AGENTS.md`), checker policy (`ruff.toml`, `mypy.ini`, `pytest.ini`),
   documentation structure (`docs/`, `zensical.toml`), a smoke test and ignore
   rules. It never renders `main.py`, `pyproject.toml`, `uv.lock` or
   `.python-version`.
2. **Standalone checker files.** Ruff, mypy and pytest are configured in their own
   files rather than in `[tool.*]` sections of `pyproject.toml`, so template content
   never lands inside a uv-owned file and no file declares a dependency twice.
3. **The repository root is the template source.** `copier.yml` sits at the devkit
   root and uses `_subdirectory` to render only
   `templates/python-script-overlay/template/`. Copier therefore treats the
   repository as a git template source, records `_src_path` and `_commit`, and can
   check out a release tag. No separate template repository, no hand-maintained
   version table, and `.copier-answers.yml` is rendered for the same reason.
4. **One documented project-owned edit.** The pinned uv generates
   `def main():` without a return annotation, which `mypy --strict` rejects. The
   creation recipe and the integration test add `-> None` as an explicit
   project-owned change. Copier does not patch application code, and the type-check
   standard is not relaxed.
5. **The single Python owner survives without touching `pyproject.toml`.** The
   generated `mise.toml` sets `UV_NO_MANAGED_PYTHON=1` and
   `UV_PYTHON_DOWNLOADS=never`, and no `.python-version` is created.
   `UV_PYTHON_PREFERENCE` is deliberately absent: uv rejects it together with
   `UV_NO_MANAGED_PYTHON`.
6. **Dependencies are installed by uv, not rendered.** The recipe installs the
   release's baseline tools with `uv add --dev` and exact `==` versions, so
   `pyproject.toml` and `uv.lock` stay uv-owned and the versions are reviewable in
   the release's documentation.
7. **Checks run sequentially in generated projects.** `[settings] jobs = 1` in the
   generated `mise.toml` prevents a fresh checkout from creating `.venv` from
   several `uv run` processes at once; it needs no custom runner.
8. **Provenance is tested with a temporary tagged repository.** ai-devkit has no
   release tag, so `mise run test-template` builds a tagged repository from
   `copier.yml` and `templates/` and asserts the recorded `_commit`. No real tag is
   created, moved or pushed.

## Consequences

- An overlay update cannot overwrite application code, manifests or lockfiles,
  which makes the native `copier update` workflow safe to document.
- Template content changes and dependency changes never collide in the same file.
- The devkit root now describes a template as well as a toolchain; readers must
  know that `_subdirectory` limits rendering to one directory.
- The scaffold's missing annotation is a visible, versioned step. When uv annotates
  its scaffold, the step becomes a no-op that the recipe asserts against.
- `mise run test-template` needs the package index and is kept out of
  `mise run check`; CI must run both.

## Alternatives considered

- **A separate template repository.** Rejected: a second version stream to tag and
  keep in step with the devkit, for one small overlay.
- **A hand-written version file instead of `.copier-answers.yml`.** Rejected:
  duplicates what Copier already records and breaks `copier update`.
- **Rendering `pyproject.toml` to add `[tool.ruff]` sections.** Rejected: two writers
  for one file, and every `uv add` would produce a template conflict.
- **A Copier task that patches `main.py` or installs dependencies.** Rejected: setup
  hooks that execute commands, plus template ownership of application code.
- **Relaxing mypy to accept the unannotated scaffold.** Rejected: it trades a real
  defect detector for a green check.
