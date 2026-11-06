# Initialize OpenSpec in a project

OpenSpec is initialized by its own CLI. There is no devkit command for it, because
a second wrapper would be a second owner of the same files.

Run this in the project root — a generated Python project, or this repository:

```bash
mise install                                          # OpenSpec and Node.js are pinned
mise exec -- openspec init --tools opencode,codex --profile core
```

Use the plain `openspec init --tools opencode,codex --profile core` form when OpenSpec
is already on `PATH` with the pinned version; `mise exec --` guarantees it.

Then commit the result:

```bash
git add openspec .opencode .agents
git status --short
```

## What initialization writes

| Path | Contents |
|---|---|
| `openspec/config.yaml` | schema (`spec-driven`) and optional project rules |
| `openspec/specs/` | behavioral specifications, written by `openspec archive` |
| `openspec/changes/` | proposed changes, written by `openspec new change` |
| `.opencode/commands/opsx-*.md` | six OpenCode slash commands |
| `.opencode/skills/openspec-*/SKILL.md` | six OpenCode skills |
| `.agents/skills/openspec-*/SKILL.md` | six Codex skills, with `.openspec-target` = `codex` |

Initialization does not touch `AGENTS.md`, `.gitignore`, `main.py`,
`pyproject.toml` or `mise.toml`. Anything else in the project stays as it was.

## Select a different agent integration

Replace the `--tools` list. The accepted names come from
`openspec init --help`; the ones this devkit documents are:

| Harness | Command | Generated files |
|---|---|---|
| OpenCode and Codex | `openspec init --tools opencode,codex --profile core` | `.opencode/`, `.agents/skills/` |
| OpenCode only | `openspec init --tools opencode --profile core` | `.opencode/` |
| Codex only | `openspec init --tools codex --profile core` | `.agents/skills/` |
| Cline (optional) | `openspec init --tools cline --profile core` | `.clinerules/workflows/`, `.cline/skills/` |

Codex receives skills only; OpenSpec prints `Commands skipped for: codex (uses
skills)`. Do not expect a Codex slash command, and do not create one by hand.

Adding a harness later is the same command with the additional name; OpenSpec keeps
the integrations it already wrote. The
[OpenSpec reference](../reference/openspec.md) lists the exact invocation for each
harness.

## Update the generated integrations

After changing the pinned OpenSpec version in `mise.toml` and running `mise install`:

```bash
mise exec -- openspec update
```

`openspec update` rewrites the generated commands and skills from the installed
package. It does not touch `openspec/specs/`, `openspec/changes/` or `AGENTS.md`.

```bash
mise exec -- openspec update --dry-run     # report the files it would change
mise exec -- openspec update --force       # rewrite even when it looks current
```

`--dry-run` also reports the global profile entry at
`$XDG_CONFIG_HOME/openspec/config.json`, which OpenSpec maintains separately from the
project. That file is your own configuration: review what `update` proposes there
instead of accepting it blindly, and never commit it.

Three rules keep the integration honest:

- Never hand-edit `.opencode/`, `.agents/skills/` or `.clinerules/workflows/`;
  the next `openspec update` overwrites the edit.
- Never copy another project's generated files; they belong to that project's
  OpenSpec version.
- Keep the Copier overlay free of them; the
  [generated-project reference](../reference/generated-project.md) explains why.

## User-level configuration stays user-level

OpenSpec keeps a global profile and telemetry state in
`$XDG_CONFIG_HOME/openspec/config.json`. `openspec init --profile core` sets the
profile for the project being initialized; it does not rewrite that file. Read it with
`openspec config list` if you need to know the global default, and change it only when
you mean to change your own environment.

The integration test runs OpenSpec with a throwaway `XDG_CONFIG_HOME` for this
reason: a test may not read or write your configuration.
