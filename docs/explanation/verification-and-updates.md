# Why verification and updates share one command

Three decisions look separate but rest on the same idea: a claim about this
configuration should be executed, not asserted in prose. CI runs the same tasks a
developer runs, a template update is a reviewed change rather than a refresh, and
project-owned files stay outside the overlay. Each follows from one owner per
concern.

## Why CI runs the local tasks

A pipeline that reimplements verification slowly grows a second definition of
"correct". The workflow could call `ruff`, `mypy` and `pytest` directly; then a task
gains a flag, the two definitions diverge, and a green pull request stops meaning
what `mise run check` means.

So `.github/workflows/verify.yml` installs the locked toolchain and then runs
`mise run check` and `mise run test-template`. That gives one definition of
verification, in `mise.toml`, with two entry points:

```text
mise.toml [tasks]  ──►  mise run check          (developer, local)
                   └──►  mise run check          (GitHub Actions)
```

The consequence is a constraint as well as a benefit: everything CI must do has to
be expressible as a task, so anything a developer cannot reproduce locally has no
place in the pipeline. That is why the workflow holds no credentials, no model call
and no platform-specific script — none of them could be run the same way on a
laptop.

The pipeline is also read-only. A verification job that can write to the repository
can repair what it is supposed to report, and a job that can write is a job whose
green state no longer means the change is correct. `contents: read` plus a final
`git status --porcelain` check makes "verification changed nothing" a checked
property instead of a hope.

## Why a template update is a reviewed change

A Copier update renders the newer template over a diff of your project. That makes
it a merge, and a merge is a change someone approves — not a refresh someone
performs.

Two consequences follow. First, the update needs a clean, committed baseline:
without one there is no "before" to merge against, which is why `copier update`
refuses a dirty tree. Second, an update touching `ruff.toml`, `mypy.ini` or
`AGENTS.md` changes your verification standard or your engineering rules. Those are
decisions, not maintenance, so the diff goes through review like any other change.

When the template and the project change the same region, Copier reports a conflict
rather than choosing. This is deliberate on both sides: Copier cannot know which
intent is current, and a tool that silently picks one turns a reviewable merge into
invisible drift. The integration test asserts exactly that — conflict markers in the
file, unmerged stages in Git, both sides' text present — so a future Copier release
that resolves such a conflict on its own would fail the test and force a
conversation.

## Why project-owned files must stay independent

The overlay renders policy: how to lint, how to type-check, where tests live, how
the site is built, what the engineering rules are. It never renders resolution or
application behavior: `main.py`, `pyproject.toml`, `uv.lock`, `.python-version`.

The reason is write ownership, not taste. `pyproject.toml` is rewritten by uv
whenever a dependency changes. If the template also rendered it, every `uv add`
would produce a template conflict, and every template update would produce a
dependency conflict — the same file with two writers. `main.py` is worse: its
changes have reasons the template cannot know, so a template that owned it would
overwrite real work.

That is what makes the update promise checkable. The lifecycle test edits `main.py`,
adds a regression test, adds a documentation page and edits an overlay-owned entry
point, then updates to a newer revision and asserts byte equality. A template that
ever started rendering application code or a dependency manifest would fail that
test on the first run.

The same boundary explains why `.copier-answers.yml` is the only version record: it
is Copier's own provenance, and a second version table would be a second owner that
drifts from the tool that applies the update.

## What this costs

- Verification is only as good as the tasks. A check that exists in the workflow
  but not in `mise run check` is a check nobody runs locally.
- The integration test is the slow half of the pipeline: it installs a project's
  dependencies and drives real tools, so it needs the package index and about a
  minute of runner time.
- Reviewed updates mean a human reads the diff. That is the point, and it is also
  work.
- The lifecycle is proven between two temporary tags, not between published
  releases, because this repository publishes none yet. The guarantee is the same
  one a released tag would give; the tag itself is not claimed.
