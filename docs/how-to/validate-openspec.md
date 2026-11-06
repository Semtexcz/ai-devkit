# Validate changes and specifications

Native OpenSpec validation is the last check in `mise run check`, so a malformed
specification fails the same command a reviewer runs. This guide covers running it
directly and fixing what it reports.

## Run the check the project uses

From a project root, including a generated Python project:

```bash
mise run spec-check      # openspec validate --all --strict --no-interactive
```

Or call the CLI directly:

```bash
mise exec -- openspec validate --all --strict --no-interactive
```

| Flag | Effect |
|---|---|
| `--all` | every change and every specification |
| `--changes` / `--specs` | only one kind |
| `--archived` | report archived changes that still have open tasks |
| `--strict` | requirements need scenarios and a purpose, in addition to structure |
| `--no-interactive` | never prompt, so a task runner can call it |

One item is enough to narrow the output:

```bash
mise exec -- openspec validate add-greeting-name --strict
mise exec -- openspec show add-greeting-name
```

## Read the result

A pass looks like this:

```text
✓ change/add-greeting-name
Totals: 1 passed, 0 failed (1 items)
```

A failure is one line per finding, with the artifact and the field it came from, and
the command exits non-zero. Two results mean something other than a failure:

- `No items found to validate.` means the scope was empty — nothing was checked.
  A project that has just run `openspec init` looks like this.
- `No OpenSpec root found from the current directory.` means the command ran outside
  an initialized project. Run `openspec init --tools opencode,codex --profile core`
  first; a missing root is not a specification error.

## Resolve the common failures

| Finding | Cause | Fix |
|---|---|---|
| `Requirement must have at least one scenario` | a `### Requirement:` heading without a `#### Scenario:` | add a scenario with `- **WHEN**` and `- **THEN**` lines |
| `Purpose must be at least 50 characters` | a new capability's delta has no `## Purpose` section, or a stub | state what the capability is for in one or two sentences |
| `Why section must be at least 50 characters` | the proposal's `## Why` is a fragment | write the motivation as a sentence, as a warning it does not fail strict validation |
| `Change must have at least one delta` | a change with no capability listed | either add the delta spec, or set `skip_specs: true` in the change's `.openspec.yaml` when the change genuinely alters no requirement (a docs-only or tooling change) |
| `Unknown schema` | `openspec/config.yaml` names a schema this version does not ship | keep `schema: spec-driven` unless you have written and installed a schema |

Fix the artifact rather than the check. Deleting a scenario, lowering the
specification's claim, or adding `skip_specs: true` to silence a real behavior change
turns the validation into decoration.

## Verify the failure path on purpose

A check that never fails proves nothing. In a throwaway project — never in a
repository you intend to keep — add a requirement without a scenario:

```bash
mkdir -p openspec/specs/invalid-example
printf '# invalid-example Specification\n\n## Purpose\n\nTemporary probe spec.\n\n## Requirements\n\n### Requirement: No scenario\n\nProse only.\n' > openspec/specs/invalid-example/spec.md
mise run check            # must fail
rm -r openspec/specs/invalid-example
mise run check            # must pass again
```

`mise run test-template` performs exactly this sequence in a temporary generated
project, so the failure path stays covered.
