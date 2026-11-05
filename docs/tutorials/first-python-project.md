# Create your first Python project

This tutorial creates one complete, verified Python script project: native
`uv init` creates the application, the ai-devkit [Copier](../reference/generated-project.md)
overlay adds shared engineering standards and documentation, and `uv` installs the
release's baseline development tools. It takes a few minutes and finishes with
`mise run check` passing inside the new project.

The commands below are the ones the integration test executes; see
[Generated project: commands and contents](../reference/generated-project.md) for
the reference view.

## Before you begin

You need:

- Linux x86-64. This is the only verified platform.
- A checkout of ai-devkit with the pinned toolchain installed:

  ```bash
  mise install --locked
  mise exec -- uv sync --locked
  ```

- Git, for the optional last step.
- A parent directory where the project can live, outside the ai-devkit checkout.
  Spaces in the path are fine and are covered by the integration test.

Every command starts from the ai-devkit checkout unless it says otherwise.

## Step 1: create the application with native `uv init`

```bash
cd /path/to/ai-devkit
mise exec -- uv init --app --no-package --no-workspace --no-pin-python \
  --no-readme --vcs none "$HOME/projects/my script"
```

Each flag is deliberate:

| Flag | Why |
|---|---|
| `--app` | an application, not a library |
| `--no-package` | unpackaged: nothing is built or published |
| `--no-workspace` | standalone, never a member of a parent workspace |
| `--no-pin-python` | no `.python-version`; `mise.toml` owns the interpreter |
| `--no-readme` | the overlay supplies the README, so uv must not create one |
| `--vcs none` | you decide when the project becomes a Git repository |

uv creates exactly two files, and neither of them is a template of this project:

```text
my script/
├── main.py            runnable entry point
└── pyproject.toml     project metadata, no dependencies yet
```

By default, `uv init` would create a packaged application and a workspace member;
the flags above prevent both.

## Step 2: apply the shared overlay with Copier

```bash
devkit="$PWD"
mise exec -- uv run --locked copier copy --vcs-ref HEAD --defaults \
  "$devkit" "$HOME/projects/my script"
```

`--vcs-ref HEAD` renders the current checkout. Use a tagged release instead once
one exists:

```bash
mise exec -- uv run --locked copier copy --vcs-ref v0.1.0 --defaults \
  gh:Semtexcz/ai-devkit "$HOME/projects/my script"
```

ai-devkit has no release tag yet, so the `gh:` form is documented but unverified;
the tag mechanism itself is exercised by `mise run test-template`, which builds a
temporary tagged repository.

!!! warning "Use a tag for projects you intend to update"
    `--vcs-ref HEAD` renders the working tree as it is now. If that tree has
    uncommitted changes, Copier records a synthetic commit in
    `.copier-answers.yml`, and a later `copier update` fails with
    `ValueError: Unknown revision`. Projects that should receive overlay updates
    must be created from a tagged release, or at least from a clean commit that
    exists in the template repository.

Copier asks two questions. `--defaults` accepts them, `project_name` defaults to
the destination directory name, and both only affect documentation:

```bash
mise exec -- uv run --locked copier copy --defaults \
  -d project_name="My script" -d project_description="Prints a greeting." \
  --vcs-ref HEAD "$devkit" "$HOME/projects/my script"
```

The overlay adds standards, checker configuration, documentation seeds and ignore
rules. It never renders `main.py`, `pyproject.toml`, `uv.lock` or
`.python-version`; see [Who owns which file](../explanation/generated-project-ownership.md).

## Step 3: install the baseline development dependencies

```bash
cd "$HOME/projects/my script"
mise exec -- uv add --dev 'ruff==0.17.3' 'mypy==2.4.1' 'pytest==9.2.0' 'zensical==0.0.74'
```

The overlay renders no dependency manifest on purpose. `uv add` writes the exactly
pinned versions into `[dependency-groups] dev` in `pyproject.toml` and resolves
`uv.lock`. Those four commands are the release's baseline; they are recorded here
so the versions are reviewable next to the code that depends on them.

## Step 4: make the one project-owned edit

`mypy --strict` is the type-checking baseline, and the scaffold uv produced does
not satisfy it:

```python
def main():
```

Add the return annotation to `main.py`:

```bash
python3 - <<'PY'
from pathlib import Path

path = Path("main.py")
text = path.read_text(encoding="utf-8")
assert "def main():\n" in text, "the uv scaffold changed; review this edit"
path.write_text(text.replace("def main():\n", "def main() -> None:\n", 1), encoding="utf-8")
PY
```

The result:

```python
def main() -> None:
    print("Hello from my-script!")
```

This is a project-owned edit to project-owned code, which is exactly why Copier
does not make it. A template that rewrote `main.py` would own application code and
would fight your later edits during `copier update`. The alternative — relaxing
mypy to accept an unannotated function — would trade a real defect detector for a
green check.

## Step 5: lock the tool versions

```bash
mise run lock-tools      # runs `mise lock`
```

This writes `mise.lock` for the pinned Python and uv, including checksums and
download URLs. Commit it once the project is a Git repository, then
`mise install --locked` installs only those versions. The step needs network
access for checksum provenance, and it is verified manually rather than by
`mise run test-template`.

## Step 6: run and verify the project

```bash
mise exec -- uv run --locked python main.py
mise exec -- uv run --locked pytest
mise run check
```

Expected output of the first command is the greeting from `main.py`. The second
runs the smoke test, which executes `main.py` as a subprocess and asserts that it
succeeds and prints something — it does not assert the greeting text.

`mise run check` runs the verification contract:

```text
uv lock --check
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy --strict main.py
uv run --locked pytest
uv run --locked zensical build --strict
```

All six must pass. There is deliberately no OpenSpec validation yet: OpenSpec is
initialized in a later task.

## Step 7: put the project under version control

```bash
git init
git add --all
git commit -m "Create the project from uv init and the ai-devkit overlay"
```

Commit `uv.lock`, `mise.lock`, `.copier-answers.yml`, `AGENTS.md` and `docs/`. The
generated `.gitignore` already excludes `.venv/`, caches, `site/` and `.env`. A Git
repository with a clean tree is also the prerequisite for later
[Copier updates](../how-to/update-project-overlay.md).

## What you have now

| Layer | Owns |
|---|---|
| `uv init` and uv | `main.py`, `pyproject.toml`, `uv.lock`, `.venv/` |
| mise | `mise.toml`, `mise.lock`, the tasks |
| Copier overlay | `AGENTS.md`, checker configuration, `docs/`, `tests/`, `.gitignore`, `.copier-answers.yml` |

Read [Who owns which file](../explanation/generated-project-ownership.md) for the
reasoning, and the
[generated project reference](../reference/generated-project.md) for every task and
version.

## Known limitations

- Linux x86-64 is the only verified platform; `mise.lock` covers `linux-x64`.
- No ai-devkit release tag exists yet, so only the `--vcs-ref HEAD` form has been
  run in this repository. Tag-based provenance is verified with a temporary
  tagged repository.
- The project is an unpackaged application; there is no build backend and nothing
  is published.
- `mise run test-template` does not create `mise.lock`; it needs network access.
- Specifications and change checklists are not part of this workflow yet.
