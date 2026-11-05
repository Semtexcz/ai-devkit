# Update a project's overlay

A generated project records the template it came from in `.copier-answers.yml`.
That file is the only input Copier needs to apply later overlay changes while
keeping project-owned edits. This guide covers the native update workflow; ai-devkit
adds no updater of its own.

## Before you start

1. The project is a Git repository with a clean working tree.

   ```bash
   git status --short      # must print nothing
   ```

2. `.copier-answers.yml` is committed and unmodified. It records `_src_path` and
   `_commit`.
3. Copier is at the version this devkit pins, 9.19.1:

   ```bash
   mise exec -- uv run --locked copier --version
   ```

   Run that from the ai-devkit checkout. Any other environment must provide the same
   Copier version, for example `uvx copier@9.19.1`.

## See whether an update exists

```bash
mise exec -- uv run --locked copier check-update <path to project>
```

The output is either `Project is up-to-date!` or the current and latest template
versions.

## Apply an update

```bash
mise exec -- uv run --locked copier update <path to project>
```

Copier checks out the newest template tag, replays the answers recorded in the
project, renders the newer template into a temporary copy, and applies the
difference to the project. Add `--vcs-ref` to pin a specific release:

```bash
mise exec -- uv run --locked copier update --vcs-ref v0.2.0 <path to project>
```

Two properties matter:

- `main.py`, `pyproject.toml`, `uv.lock` and `.venv/` are never rendered by the
  template, so an update cannot overwrite them.
- Overlay files you edited (for example `AGENTS.md` or a documentation page) can
  conflict. Copier reports the conflict instead of silently choosing a side.

## Resolve conflicts

`--conflict inline` (the default) writes merge markers into the file; `--conflict
rej` writes `.rej` files next to it. Resolve by hand, keep your project's intent
where the two disagree, and never commit conflict markers.

If an update goes wrong, discard it and start again:

```bash
git checkout .
git status --short      # must print nothing
```

`copier recopy` is the fallback when the diff cannot be applied at all. It rewrites
overlay files from the template and keeps your answers, so review the result as if
it were a fresh overlay.

## Troubleshooting

`ValueError: Unknown revision: '<sha>'` means the project was created from an
uncommitted template working tree, so `_commit` records a synthetic commit that the
template repository does not contain. Copier cannot diff against it. Create the
project again from a tagged release, or from a clean commit, and copy your project
files across.

`DirtyLocalWarning` or a request to commit means the project tree is not clean.
Commit or stash first: Copier applies a diff and needs a known baseline.

## Verify afterwards

```bash
cd <path to project>
mise run check
```

Review the diff before committing. An update that changes checker configuration is a
change to your verification standard, so it deserves an explicit look.

## Known limitations

- ai-devkit has no release tag yet. Until one exists, `--vcs-ref HEAD` is the only
  working reference, and a HEAD copy of a dirty working tree records a synthetic
  commit rather than a released version.
- Conflict-preserving update behavior across tagged releases, including that an
  edited application and edited documentation survive, is lifecycle testing that a
  later task covers. This task verifies that provenance is recorded and that a clean
  update applies without touching project-owned files.
- Rolling back an overlay is a Git revert of the update commit, not an edit of
  `.copier-answers.yml`.
