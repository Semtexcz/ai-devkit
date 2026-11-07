# OpenSpec: commands, generated files and validation

Reference for the OpenSpec integration in this repository, verified against the
pinned **OpenSpec 1.16.0** (`mise exec -- openspec --version`). Upstream
documentation is canonical for anything not listed here:
<https://github.com/Fission-AI/OpenSpec>.

OpenSpec owns behavioral requirements and change task lists. It is initialized
natively; this repository adds no wrapper, no schema and no second backlog.

## Initialization

```bash
mise exec -- openspec init --tools opencode,codex --profile core
```

| Flag | Effect |
|---|---|
| `--tools` | comma-separated harness list; `all`, `none`, or names such as `opencode`, `codex`, `cline` |
| `--profile core` | the default workflow set: propose, explore, apply, update, sync, archive |
| `--language` | language for new artifacts, if not English |

`--profile` applies to the project being initialized. The global profile in
`$XDG_CONFIG_HOME/openspec/config.json` is user-level configuration: `openspec init`
does not rewrite it, and no repository setting overrides it.

The same command initializes a generated Python project, which then owns its own
`openspec/` directory. A project never inherits this repository's specifications.

## Generated files and their owner

Initialization with `--tools opencode,codex` produced exactly these paths:

| Path | Owner | Commit it |
|---|---|---|
| `openspec/config.yaml` | OpenSpec | yes |
| `openspec/specs/` | OpenSpec, written by `archive` | yes |
| `openspec/changes/` | OpenSpec, written by `new change` | yes |
| `.opencode/commands/opsx-*.md` | OpenSpec `init` / `update` | yes |
| `.opencode/skills/openspec-*/SKILL.md` | OpenSpec `init` / `update` | yes |
| `.agents/skills/openspec-*/SKILL.md` | OpenSpec `init` / `update` | yes |
| `.agents/skills/.openspec-target` | OpenSpec `init` / `update` | yes |

The six core workflows are `propose`, `explore`, `apply`, `update`, `sync` and
`archive`. Initialization reports `6 skills and 6 commands in .opencode, .agents/`
and `Commands skipped for: codex (uses skills)`: Codex is served by skills in
`.agents/skills/`, OpenCode by both `.opencode/commands/` and `.opencode/skills/`.

Nothing in that table is rendered by the Copier overlay, and the overlay carries no
copy of it. The integration test asserts both facts, so a template change cannot
introduce a second owner.

## Invoking a workflow

The names below are copied from the generated files, not guessed:

| Harness | Invocation | Source file |
|---|---|---|
| OpenCode | `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, `/opsx-explore`, `/opsx-sync`, `/opsx-update` | `.opencode/commands/opsx-*.md` |
| Codex | `$openspec-propose`, `$openspec-apply-change`, `$openspec-archive-change`, `$openspec-explore`, `$openspec-sync-specs`, `$openspec-update-change` | `.agents/skills/openspec-*/SKILL.md` (`name:` field) |
| Cline (optional) | `/opsx-propose` and the other `opsx-*` workflows | `.clinerules/workflows/opsx-*.md` and `.cline/skills/` |

Each skill's `description` also gives conversational triggers such as "openspec
propose". The Cline setup is opt-in:

```bash
mise exec -- openspec init --tools cline --profile core
```

OpenCode and Codex do not share an interface: OpenCode has slash commands *and*
skills, Codex has skills only. Use the form the file actually provides.

`AGENTS.md` stays harness-agnostic: it names no model, provider or command syntax.

## CLI commands used here

| Command | Purpose |
|---|---|
| `openspec init --tools <list> --profile core` | create the project structure and the harness integrations |
| `openspec update` | refresh generated integration files after an OpenSpec upgrade |
| `openspec new change <name>` | create `openspec/changes/<name>/` |
| `openspec status --change <name>` | which artifacts exist; `--json` for machine use |
| `openspec list` | changes; `--specs` lists specifications; `--json` includes the resolved root |
| `openspec validate <name> --strict` | validate one change |
| `openspec validate --all --strict --no-interactive` | validate every change and specification |
| `openspec validate --archived --strict` | report archived changes that still have open tasks |
| `openspec archive <name>` | move a change to `archive/` and update the main specification |

`openspec instructions <artifact> --change <name>` prints the enriched authoring
guide for one artifact, and `openspec templates` prints the resolved template paths.
Both read the installed package, so they always describe the pinned version.

## Validation

```bash
mise exec -- openspec validate --all --strict --no-interactive
```

`--strict` adds the checks that make a specification worth reading: a requirement
needs at least one scenario, and a new capability needs a `## Purpose` section.
`--no-interactive` disables prompts so the command works in a task runner.

The same command is the OpenSpec entry in `mise run check`, in this repository and
in a generated project (`mise run spec-check`). The two check sets differ in size —
four tasks here, seven in a generated project — and this is one of each. No custom
parser is involved, and a specification that OpenSpec rejects makes the check exit
non-zero.

Two native behaviors are worth knowing:

- **No root, no validation.** Outside an initialized project the command exits
  non-zero with `No OpenSpec root found from the current directory.` A project must
  therefore be initialized before its first `mise run check`.
- **An empty scope passes.** A project whose `openspec/specs/` and
  `openspec/changes/` contain no items prints `No items found to validate.` and exits
  zero. That result says nothing about validation working; the first real
  specification is the evidence.

## Specification format

Main specifications live in `openspec/specs/<capability>/spec.md` and are written by
`openspec archive`, not by hand. A change supplies a delta in
`openspec/changes/<name>/specs/<capability>/spec.md`:

```markdown
## Purpose

One or two sentences on what the capability is for. Required for a new capability.

## ADDED Requirements

### Requirement: Greeting name selection

The script SHALL greet the name supplied with `--name`.

#### Scenario: Explicit name

- **WHEN** the script runs with `--name Ada`
- **THEN** it prints `Hello from Ada!`
```

The archived main specification uses `# <capability> Specification`, then
`## Purpose`, then `## Requirements` with the same requirement and scenario
headings. `## MODIFIED`, `## REMOVED` and `## RENAMED` sections express other kinds of
change to an existing capability.

This repository's own specification is
`openspec/specs/generated-project-verification/spec.md`; the
[worked tutorial](../tutorials/spec-driven-change.md) shows the delta form in use.
