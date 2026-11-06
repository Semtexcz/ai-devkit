# Plan, implement and archive one change

This tutorial takes one small change through the whole specification-driven
workflow with [OpenSpec](https://github.com/Fission-AI/OpenSpec): propose, review,
implement, test, validate and archive. It runs inside a Python script project
created by the [first-project tutorial](first-python-project.md), because that is
where application code lives.

The change: **add a command-line `--name` argument that customizes the script's
greeting while preserving the existing default behavior.**

The example files are in `examples/openspec-change/` in this repository.
`mise run test-template` copies them into a generated project and runs the sequence
below, so these steps describe executed behavior rather than an idea.

## Before you begin

- A generated project from [Create your first Python project](first-python-project.md),
  with OpenSpec initialized:

  ```bash
  mise install
  openspec init --tools opencode,codex --profile core
  ```

- `mise run check` passes before you start. A change is easier to review against a
  green baseline.

Every command runs inside the project unless it says otherwise.

## Step 1: propose the change

```bash
openspec new change add-greeting-name
openspec status --change add-greeting-name
```

With OpenSpec's agent integration you can let the harness write the artifacts
instead: `/opsx-propose "add a --name argument to the greeting"` in OpenCode,
`$openspec-propose` in Codex, `/opsx-propose` from Cline's workflow list. Either
way, read what you got before implementing it.

## Step 2: review the proposal

`openspec/changes/add-greeting-name/proposal.md` states why the change exists. This
example's proposal is short on purpose:

- **Why** — the greeting cannot be personalized without editing `main.py`.
- **What changes** — an optional `--name` argument; without it the output is
  unchanged.
- **New capability** — `greeting`, which owns the requirement in step 3.
- **Impact** — `main.py`, one new test, one documentation page, no new dependency.

Review means asking whether the change is small enough to finish in one review, and
whether it touches more capabilities than it claims.

## Step 3: state the behavioral requirement

The delta spec lives at
`openspec/changes/add-greeting-name/specs/greeting/spec.md`:

```markdown
## Purpose

The greeting capability decides which name the script addresses and what it prints.

## ADDED Requirements

### Requirement: Greeting name selection

The script SHALL greet the name supplied with `--name`, and SHALL print the
default greeting when the argument is absent.

#### Scenario: Explicit name

- **WHEN** the script runs with `--name Ada`
- **THEN** it prints `Hello from Ada!`

#### Scenario: Default greeting is preserved

- **WHEN** the script runs without `--name`
- **THEN** it prints the same greeting it printed before the argument existed
```

Two properties matter. The requirement is about observable behavior — what the
script prints — not about `argparse`. And the second scenario exists because
"preserve the default" is the part of this change that is easiest to break.

## Step 4: write the implementation tasks

`openspec/changes/add-greeting-name/tasks.md` lists the work as checkboxes:

```markdown
## 1. Implementation

- [ ] 1.1 Read `main.py` and record the greeting it prints today
- [ ] 1.2 Add the `--name` argument with `argparse`, keeping the annotation on `main`
- [ ] 1.3 Run the script with and without `--name`
```

OpenSpec owns this list. Do not mirror it in a second file: `openspec status` is the
progress report.

## Step 5: validate before implementing

```bash
openspec validate add-greeting-name --strict --no-interactive
```

Expected output: `Change 'add-greeting-name' is valid`. A malformed requirement fails
here, before any code is written — that is the point of validating early.

## Step 6: implement the change

The changed entry point, `examples/openspec-change/main.py`, uses the standard
library only:

```python
DEFAULT_NAME = "script-project"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Return the parsed command line."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        default=DEFAULT_NAME,
        help=f"name to greet (default: {DEFAULT_NAME})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Print the greeting."""
    args = parse_args(argv)
    print(f"Hello from {args.name}!")
```

`DEFAULT_NAME` is the name the scaffold already greeted, which is how the default
scenario keeps passing. The annotation on `main` stays: `mypy --strict` requires it.

## Step 7: add the regression test

`examples/openspec-change/tests/test_greeting.py` runs the script as a subprocess and
asserts both scenarios:

```python
def test_explicit_name_is_greeted() -> None:
    assert _greeting("--name", "Ada") == "Hello from Ada!\n"


def test_default_greeting_is_unchanged() -> None:
    assert _greeting() == "Hello from script-project!\n"
```

The existing smoke test in `tests/test_main.py` stays: it proves the script still
runs, and it does not need to change when the message does.

## Step 8: update the documentation

Add the new behavior to the page a reader would open,
`docs/tutorials/run-the-script.md`:

```markdown
## Greet a name from the command line

`main.py` accepts `--name`, so the greeting does not need a source edit:

    uv run --locked python main.py --name Ada
```

A change that alters user-visible behavior without changing its page is incomplete,
and `mise run docs` would still pass — that check catches broken links, not missing
paragraphs.

## Step 9: validate again

```bash
openspec validate add-greeting-name --strict --no-interactive
```

The artifacts have not changed since step 5; the re-run proves the change is still
the change you validated.

## Step 10: run the verification contract

```bash
mise run check
```

All seven checks run, including `openspec validate --all --strict --no-interactive`.
A failure here is a failure of the change, not of the tool: fix the cause instead of
relaxing `ruff.toml`, `mypy.ini` or `pytest.ini`.

## Step 11: review against the specification

Read the requirement and each scenario, and confirm the test that proves it. Then
mark the task complete in `tasks.md`:

```markdown
- [x] 1.2 Add the `--name` argument with `argparse`, keeping the annotation on `main`
```

`openspec status --change add-greeting-name` reports artifact progress, and
`openspec validate --archived` reports a change archived with open tasks. A box is
ticked when the work is verified, not when the code is typed.

## Step 12: archive the accepted change

```bash
openspec archive add-greeting-name
mise run check
```

Archiving does three things:

1. moves the change to `openspec/changes/archive/<date>-add-greeting-name/`;
2. writes the requirement from the delta into `openspec/specs/greeting/spec.md`, so
   the specification now describes the project as it is;
3. keeps the archived artifacts as the record of why the requirement exists.

The second `mise run check` proves the project still verifies with the main
specification in place.

## What you have now

| Artifact | Contents |
|---|---|
| `openspec/specs/greeting/spec.md` | the behavior the project promises today |
| `openspec/changes/archive/<date>-add-greeting-name/` | proposal, delta and tasks: the reasoning |
| `main.py`, `tests/test_greeting.py` | the implementation and its regression test |
| `docs/tutorials/run-the-script.md` | how a reader uses the new argument |

Nothing else was created: no backlog file, no status table, no task database. The
next change starts at step 1.

To read about the division of labor, see
[OpenSpec, AGENTS.md and ADRs](../explanation/openspec-and-agents.md). For the
commands without the narrative, see the [OpenSpec reference](../reference/openspec.md).
