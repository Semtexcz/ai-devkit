# OpenSpec, AGENTS.md and ADRs: three kinds of written rule

Three files in this repository look like instructions, and confusing them is the
usual reason a project grows a fourth. Each answers a different question and has a
different lifespan.

| Artifact | Answers | Written by | Changes when |
|---|---|---|---|
| `AGENTS.md` | *How do we work here?* | the devkit, per project | the engineering standard changes |
| `openspec/specs/` | *What must the system do?* | OpenSpec, from archived changes | a requirement is accepted |
| `openspec/changes/<name>/` | *What are we doing now, and why?* | you, per change | one change exists and then is archived |
| `docs/explanation/decisions/` | *Why is it built this way?* | a human, per decision | a decision is revisited |

## AGENTS.md is a standard, not a plan

`AGENTS.md` states the rules that outlive any single change: reuse before building,
small reviewable diffs, every behavior change covered by a test, never weaken a check,
keep documentation in step. It names no feature, no model and no provider, so it can
be read by any harness and stays true next release.

Putting a task list there would mean rewriting shared policy for every feature. That
is why the shared file says what "done" means and not what is next.

## OpenSpec requirements are observable promises

A requirement states behavior someone can check: *the script SHALL greet the name
supplied with `--name`, and SHALL print the default greeting when the argument is
absent.* Its scenarios name the observation, so the requirement can be tested and
re-read after the implementation is forgotten.

Two consequences follow:

- A requirement describes behavior, not design. `argparse` is an implementation
  choice; it belongs in the change's design section or in the commit, not in the
  requirement.
- A requirement outlives the change that introduced it. Archiving moves it into
  `openspec/specs/`, where the next change must respect it — or explicitly modify it
  with a `## MODIFIED` delta.

## Change tasks are a plan with an end

`tasks.md` inside a change is a checklist for that change only: implementation,
test, documentation, validation. It is not a backlog. When the change is archived the
task list is evidence of what was done, not a queue of remaining work.

That is the reason this repository has no board, no status column and no
`.ai/state.json`: a task belongs to a change, a change belongs to a directory, and
the directory moves to `archive/` when the work is accepted. The state is the file
system.

## ADRs keep the reasoning

A requirement says *what* must be true. An ADR says *why* the project is shaped this
way, including the alternatives that were rejected. The overlay boundary, the two
lockfiles and the one documented project-owned edit are decisions of that kind: they
constrain future changes, and a requirement that contradicted them would be a bug in
the requirement.

So the split is:

- behavioral promise → `openspec/specs/`
- engineering standard → `AGENTS.md`
- architectural rationale → ADR under `docs/explanation/decisions/`
- work in progress → `openspec/changes/<name>/`

## Why no orchestrator or second tracker

Every extra layer would need its own state, its own update path and its own
consistency check against the other three. OpenSpec already validates its own
artifacts with a command that exits non-zero, and `mise run check` calls it, so a
specification that drifts from the format fails the same command that runs the tests.

What that buys:

- one authoritative place for requirements, with a native validator;
- one checklist per change, deleted from the backlog by `archive`;
- no parallel task state to reconcile, and no custom parser to maintain;
- harness independence: the generated commands belong to OpenSpec, and `AGENTS.md`
  stays true whichever agent reads it.

The trade-off is that OpenSpec's file layout and schema are not ours to change. That
is the point: the devkit configures and documents a maintained tool instead of
building one.
