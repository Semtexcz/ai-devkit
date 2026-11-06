# Worked example: add a `--name` argument

Fixture for the workflow documented in
[`docs/tutorials/spec-driven-change.md`](../../docs/tutorials/spec-driven-change.md).
It is example data, not application code of this repository and not part of the
Copier overlay: a generated project's application code belongs to that project, so
nothing here is rendered into a project.

`mise run test-template` copies these files into the generated project and runs the
whole OpenSpec lifecycle there, so the tutorial cannot drift from executed behavior.

| File here | Becomes, in the generated project |
|---|---|
| `proposal.md` | `openspec/changes/add-greeting-name/proposal.md` |
| `specs/greeting/spec.md` | `openspec/changes/add-greeting-name/specs/greeting/spec.md` |
| `tasks.md` | `openspec/changes/add-greeting-name/tasks.md` |
| `main.py` | `main.py` (the application file the change produces) |
| `tests/test_greeting.py` | `tests/test_greeting.py` (new regression test) |
| `run-the-script-addendum.md` | appended to `docs/tutorials/run-the-script.md` |

The example assumes the generated project is named `script-project`, because the
default greeting must stay exactly what the scaffold printed
(`Hello from script-project!`).
