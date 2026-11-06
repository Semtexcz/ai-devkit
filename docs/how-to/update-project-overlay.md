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

The update also rewrites `.copier-answers.yml` to the revision it applied. Review
that line together with the rest of the diff: it is the project's only record of
which overlay revision it runs.

## What an update guarantees

Each guarantee below is executed on every `mise run test-template` run, between two
temporary tagged revisions, so it is behavior rather than intention:

| Guarantee | How it is proven |
|---|---|
| Application code and project tests survive | a project edits `main.py`, adds a regression test, commits, updates, and both files are byte-identical afterwards |
| Python dependency manifests survive | `pyproject.toml` and `uv.lock` are byte-identical after the update |
| Project-owned documentation survives | a new page and the link to it are unchanged after the update |
| An overlay-owned page you edited survives, when the template did not change it | the edited page is byte-identical after the update |
| A same-region edit is visible, not silent | the update leaves inline markers, Git records the file as unresolved, and both sides' text is present |
| Provenance advances | `.copier-answers.yml` names the applied revision, keeps your source path and answers, and `copier check-update` reports the project as up to date |
| Nothing unrelated changes | only the overlay files the template changed and the answers file differ |

## Resolve conflicts

An update conflicts when the template and the project change the same region of the
same file. With Copier 9.19.1 the default `--conflict inline` writes the conflict
into the file as three marker lines around the two versions:

| Marker line | Followed by |
|---|---|
| `<<<<<<< before updating` | your project's version of the region |
| `=======` | the template's version of the region |
| `>>>>>>> after updating` | the rest of the file |

Copier removes its `.rej` witnesses after that three-way merge, so a file left
holding `.rej` artifacts means the update did not finish; see Troubleshooting.

Work through the conflict as a merge:

```bash
git status --short                 # "UU AGENTS.md": unresolved
git ls-files --unmerged AGENTS.md  # stages 1, 2 and 3: base, ours, theirs
```

1. Edit the file and keep the intent that is current. Dropping one side is a
   decision; write down why in the commit message. Never commit conflict markers.
2. Stage the resolved file, which clears the unmerged stages:

   ```bash
   git add AGENTS.md
   git ls-files --unmerged AGENTS.md   # must print nothing
   ```

3. Verify the resolved project, then commit the update as one reviewable change:

   ```bash
   mise run check
   git commit -am "chore: apply overlay update to v0.2.0"
   ```

`copier recopy` is the fallback when the diff cannot be applied at all. It rewrites
overlay files from the template and keeps your answers, so review the result as if
it were a fresh overlay — it discards local edits to overlay files.

## Discard the whole update

Resolving is the default, because the update is a reviewable diff and its conflicts
carry information. Abandon the update instead when the diff itself is the problem: a
wrong `--vcs-ref`, a template that moved further than the project can follow, or a
`recopy` you did not want. The procedure below returns the project to the commit it
was on before the update started.

`git checkout .` does not do that. A conflicting update leaves the file in Git's
unmerged state (`UU AGENTS.md`), and `git checkout .` refuses to touch an unmerged
path: it reports an error and leaves the conflict exactly where it was. Restore the
committed state instead:

```bash
git restore --source=HEAD --staged --worktree .
git status --short
```

`--source=HEAD` writes the committed content to both the working tree and the index,
which clears the unmerged stages, so Git stops reporting the file as conflicted.

!!! warning "This abandons every uncommitted change to tracked files"

    `git restore --source=HEAD --staged --worktree .` **discards all uncommitted
    changes to tracked files**, including changes you staged before the update and
    never committed. Nothing it drops can be recovered from the working tree or the
    index. Run it only when you intentionally want to abandon the entire update, and
    only in a repository whose tracked files were clean and committed before the
    update started; commit or stash anything you want to keep first.

Untracked files are a separate matter: this command does not necessarily remove
them. Copier writes new overlay files without adding them to the index, so they
appear as `??` entries and survive the restore. Read `git status --short` afterwards
and review each remaining `??` path by hand, removing the ones the discarded update
created and keeping the ones you added yourself. Do not reach for `git clean -fd`,
`git reset --hard` or any other automated cleanup: those delete paths nobody has
looked at, including files that were never part of the update.

Confirm the tree matches the commit before you retry:

```bash
git status --short        # only reviewed "??" entries may remain
git diff HEAD --stat      # must print nothing
git ls-files --unmerged   # must print nothing: no unmerged stages left
```

## Troubleshooting

`ValueError: Unknown revision: '<sha>'` means the project was created from an
uncommitted template working tree, so `_commit` records a synthetic commit that the
template repository does not contain. Copier cannot diff against it. Create the
project again from a tagged release, or from a clean commit, and copy your project
files across.

`DirtyLocalWarning` or a request to commit means the project tree is not clean.
Commit or stash first: Copier applies a diff and needs a known baseline.

A `.rej` file next to an overlay file means the patch was rejected and the inline
merge did not complete. Discard the update as described in
[Discard the whole update](#discard-the-whole-update) and run it again; if it
repeats, the template and the project have diverged too far for a diff, so resolve it
with `copier recopy` and reapply your edits by hand.

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
  commit rather than a released version. The update lifecycle is proven against
  temporary tags built from this repository's template source, not against a
  published release.
- The lifecycle is proven on Linux x86-64 with Copier 9.19.1, the version this
  devkit pins. Copier's conflict reporting is that release's behavior; a change in
  it fails the integration test rather than passing silently.
- Provenance names a revision and a source path, not a checksum of the rendered
  overlay. Reviewing the diff after an update remains the point of the procedure.
- Rolling back an overlay is a Git revert of the update commit, not an edit of
  `.copier-answers.yml`.
