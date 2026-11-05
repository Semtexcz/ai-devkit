# ai-devkit documentation

`ai-devkit` is a portable, versioned collection of development configurations,
engineering rules, documentation and a small project overlay. It composes
maintained tools instead of implementing a development framework.

This site documents the repository itself: the pinned toolchain that makes the
maintainer environment reproducible, and the standards that will be applied to
generated Python projects.

## Status

Implemented and verified in this repository:

- the engineering contract in `AGENTS.md` and the architecture decision records
  ([ADR 0001](explanation/decisions/0001-minimal-devkit.md),
  [ADR 0002](explanation/decisions/0002-script-project-overlay.md));
- a pinned, lockfile-based development toolchain (**Task 2**);
- credential-free configuration examples for OpenCode, the Codex CLI and Cline
  (**Task 3**);
- a Copier overlay that creates a verifiable Python script project from native
  `uv init` (**Task 4**), with a generation integration test;
- a Zensical documentation build with strict internal-link validation.

Planned, not implemented: OpenSpec initialization (**Task 5**), CI and Copier
update lifecycle testing (**Task 6**), clean-machine validation (**Task 7**). The
[v0.1 plan](plans/ai-devkit-v0.1.md) owns that backlog; nothing here claims those
parts work.

Agent configuration is documented, not automated: this repository ships examples
and instructions, and each harness keeps its own credentials.

## Documentation map

The documentation follows [Diátaxis](https://diataxis.fr/). Pick the section
that matches what you need:

| Section | Purpose | Start here |
|---|---|---|
| Tutorial | Learn the current setup by doing it | [Getting started](tutorials/getting-started.md) |
| How-to guide | Achieve a specific goal | [Install the development toolchain](how-to/install-toolchain.md) |
| Reference | Look up exact tools, versions and commands | [Tool ownership and pinned versions](reference/tool-versions.md) |
| Explanation | Understand why the setup is shaped this way | [Reproducibility and Python ownership](explanation/reproducibility.md) |

Creating a project: [Create your first Python project](tutorials/first-python-project.md)
walks through the whole recipe, and
[Generated project: commands and contents](reference/generated-project.md) lists
every file and task it produces.

Repository records that are not tutorial content:

- `AGENTS.md` (repository root) — engineering rules for people and coding
  agents.
- [ADR 0001](explanation/decisions/0001-minimal-devkit.md) — why the devkit is
  configuration-first.
- [ADR 0002](explanation/decisions/0002-script-project-overlay.md) — what the
  overlay may render and how provenance works.
- [ai-devkit v0.1 plan](plans/ai-devkit-v0.1.md) — approved scope and backlog.
- `examples/agents/` — credential-free OpenCode and Codex configuration
  examples, inert until copied.

Working with a coding agent starts with
[Configure coding agents](how-to/configure-coding-agents.md); exact file
locations, precedence and verified capabilities are in the
[agent configuration reference](reference/agent-configuration.md).

## Common commands

```bash
mise install --locked          # install the pinned toolchain
mise exec -- uv sync --locked  # create/update the Python environment
mise run docs                  # build the site, fail on broken links
mise run docs-serve            # preview at http://localhost:8000
mise run examples-check        # parse the agent examples (syntax only)
mise run test-template         # create and verify a project with uv + Copier
mise run check                 # every check implemented so far
```

`Linux x86-64` is the only platform this toolchain has been verified on.
