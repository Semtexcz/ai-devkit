# Agent configuration examples

Credential-free starting points for the initial harnesses. Nothing here is read
by any tool: a file becomes active only when you copy it, or its settings, to the
location named in its header.

| File | Copy to | Harness |
|---|---|---|
| `opencode.json` | `~/.config/opencode/opencode.json` | OpenCode 1.19.5 |
| `codex/ai-devkit-advanced.config.toml` | `$CODEX_HOME/ai-devkit-advanced.config.toml`, normally `~/.codex/` | Codex CLI 0.163.0 |

There is no Cline file: Cline is configured in its own interface, and its
provider settings are global.

When copying `opencode.json`, check the target directory first: OpenCode 1.19.5
creates `~/.config/opencode/opencode.jsonc` on first run, and the `.jsonc` file
wins for conflicting keys. Never overwrite an existing `opencode.json` or
`opencode.jsonc` — add the two keys to the file that is already there. The same
rule applies to the Codex profile: edit an existing file instead of replacing it.

Rules for changing these files:

- No credential, token or account identifier belongs here, in any form.
- Model identifiers are examples, not requirements. Change them with the
  harness's own mechanism, and record a new identifier in the reference only
  after verifying it against the pinned version.
- `mise run examples-check` parses both files; it is part of `mise run check`.

## Validation levels

The three levels are separate, and only the first runs automatically:

| Level | How | Status |
|---|---|---|
| Syntax | `mise run examples-check`, a standard-library JSON and TOML parse | Automated |
| CLI configuration | `opencode debug config` and `codex doctor` in a throwaway home | Verified against the pinned versions; manual |
| Authenticated execution | `opencode run --model …`, `codex exec` | Not run by this repository; the user's own sessions are recorded in the [v0.1.0 acceptance report](../../docs/releases/v0.1.0-acceptance-report.md#d2-user-provided-live-session-evidence) |

`mise run examples-check` stays a parse check so that `mise run check` remains
fast, offline and deterministic, and never touches a user configuration.

Setup steps: `docs/how-to/configure-coding-agents.md`.
Locations, precedence and verified capabilities:
`docs/reference/agent-configuration.md`.
