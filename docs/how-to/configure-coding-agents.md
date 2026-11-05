# Configure coding agents

How to configure the three initial coding agents with their own native
mechanisms, and how to change the agent, provider or model afterwards.

Nothing here installs a tool (see
[Install the development toolchain](install-toolchain.md)) and nothing here
changes your user configuration for you: every copy step is yours to run, after
you have read the file.

## Before you begin

- The pinned toolchain is installed: `mise run versions` reports OpenCode
  `1.19.5` and `codex-cli 0.163.0`.
- You have your own DeepSeek API key and/or a ChatGPT account whose plan covers
  Codex.
- The example files live in `examples/agents/`. They are inert: they are not
  read by any tool until you copy them to the location named below.

Credentials stay in each harness's own store. No example in this repository
contains a key, and no key belongs in a file that Git tracks.

## Pick the execution role first

A role is a job you are doing now, not a setting. Choose it before you start a
harness, then start the harness that fits it.

| Role | Default configuration | Rationale |
|---|---|---|
| Planner | Codex, advanced profile | Difficult reasoning, whole-repository context |
| Implementer | OpenCode or Cline, `deepseek-flash` | Bounded edits at a low token price |
| Reviewer | Codex, advanced profile | Independent review of a finished change |
| Fixer | OpenCode or Cline, `deepseek-flash` | Bounded repairs with the failure evidence |

These are recommendations, not enforced assignments: every harness is usable for
every role. There is no router, so changing role means starting a different
harness or changing its model explicitly — see
[why the devkit keeps these concepts separate](../explanation/agent-independence.md).

## Configure OpenCode with DeepSeek

1. Check what already exists, then copy the example. OpenCode 1.19.5 creates
   `~/.config/opencode/opencode.jsonc` the first time it runs, and in that
   directory a `.jsonc` file wins over a `.json` file for conflicting keys.

   ```bash
   ls ~/.config/opencode
   mkdir -p ~/.config/opencode
   cp examples/agents/opencode.json ~/.config/opencode/opencode.json
   ```

   If `opencode.jsonc` already exists, add the two keys to that file and remove
   the copy you just made — a `model` left in `opencode.json` would not take
   effect. If `opencode.json` already existed, merge into it rather than
   overwriting it.

2. Authenticate. Run OpenCode and use `/connect`, or run the provider command:

   ```bash
   opencode providers login
   ```

   The key is stored in `~/.local/share/opencode/auth.json`, not in your config
   file. As an alternative, export `DEEPSEEK_API_KEY` and OpenCode reads it from
   the environment.

3. Verify that the provider and models are visible:

   ```bash
   opencode models deepseek
   ```

   Expected output:

   ```text
   deepseek/deepseek-flash
   deepseek/deepseek-v4-pro
   ```

   A `Provider not found: deepseek` error means that shell has no DeepSeek
   credential: either the `/connect` step did not complete, or
   `DEEPSEEK_API_KEY` is not exported in this shell.

The example sets two keys and nothing else:

| Key | Value | Reason |
|---|---|---|
| `model` | `deepseek/deepseek-flash` | Economical default for implementation work |
| `small_model` | `deepseek/deepseek-flash` | Pins auxiliary work such as title generation to the same provider instead of letting OpenCode choose |

`deepseek` is a built-in provider from the models.dev catalog, so there is no
custom `provider` block. Current OpenCode documentation marks `small_model` as
deprecated; the pinned 1.19.5 release still honours it (`opencode debug config`
keeps the key). If a later release removes it, delete the key — the explicit
`model` remains in force.

### Change the OpenCode model

- For one session: `opencode -m deepseek/deepseek-v4-pro`, or `/models` inside
  the interface.
- Permanently: edit `model` in the OpenCode config file that exists —
  `opencode.jsonc` takes precedence when both files are present.
- For one project only: add `opencode.json` to that project's root. Project keys
  override global keys, and non-conflicting global keys survive.
- For another provider: connect that provider's credentials, then set `model` to
  its `provider/model` identifier. No devkit change is needed.

## Authenticate Codex with ChatGPT

1. Sign in with the subscription, not with an API key:

   ```bash
   codex login
   ```

   Complete the browser flow. Credentials are cached in `~/.codex/auth.json` or
   in your operating system credential store, depending on
   `cli_auth_credentials_store`.

2. Confirm which method is active:

   ```bash
   codex login status
   ```

   It must report the ChatGPT sign-in. On a machine without a browser, use
   `codex login --device-auth` after enabling device-code login in your ChatGPT
   security settings. Inside a session, `/status` shows the active model, the
   approval policy and the writable roots.

3. Do **not** run `codex login --with-api-key`, and do not set `OPENAI_API_KEY`,
   when subscription access is intended: both switch Codex to separately billed
   API usage. `codex logout` clears the stored credentials.

4. Diagnose configuration, authentication and runtime state:

   ```bash
   codex doctor
   ```

### Add the advanced profile

```bash
cp examples/agents/codex/ai-devkit-advanced.config.toml \
  ~/.codex/ai-devkit-advanced.config.toml

codex --profile ai-devkit-advanced
codex exec --profile ai-devkit-advanced "review the current diff"
```

A profile is a separate file next to the user config, holding top-level keys
that are layered over `~/.codex/config.toml`. Since Codex 0.134.0 the
`[profiles.<name>]` table and the `profile = "..."` selector are no longer read,
so an existing `~/.codex/config.toml` needs no edit. `--profile` applies to
runtime commands only; `codex doctor` and `codex debug` reject it.

The example sets `approval_policy = "on-request"` and
`sandbox_mode = "workspace-write"`. It deliberately sets no `model`: available
models depend on your account, so the account-supported default stays in effect.

### Override the Codex model or sandbox

```bash
codex --profile ai-devkit-advanced -m <model-id>       # one session
codex exec -c model=<model-id> "fix the failing test"  # one non-interactive run
codex --profile ai-devkit-advanced -s read-only        # review without writes
```

Use `-m` only with a model you have confirmed on your own account. `codex exec`
is non-interactive and never asks for approval, so `approval_policy` affects
interactive sessions; keep the default sandbox rather than reaching for
`--dangerously-bypass-approvals-and-sandbox`.

### Two separate billing paths

Signing in with ChatGPT uses your subscription and its account-dependent limits.
Signing in with an API key, or exporting `OPENAI_API_KEY`, is metered API
billing. The devkit never converts one into the other, and never presents
subscription usage as unlimited.

### Keep provider settings out of the project

A `.codex/config.toml` in a repository loads only for a trusted project, and
Codex ignores the keys that select credentials, providers or profiles there
(`model_provider`, `model_providers`, `profile`, `profiles`, `openai_base_url`,
`chatgpt_base_url`, `notify`, `otel`, and others). Provider and profile
configuration belongs in `~/.codex/config.toml` and
`~/.codex/<name>.config.toml`, so this repository ships no `.codex/` directory.

## Configure the optional Cline integration

Cline is optional; it is the agent this backlog was implemented with. It is
configured entirely through its own interface.

1. Open the Cline settings (⚙ in the Cline panel).
2. Set **API Provider** to `DeepSeek`.
3. Paste your DeepSeek API key.
4. Select `deepseek-flash` in the **Model** dropdown.

Provider settings are global, stored in `~/.cline/data/settings/providers.json`.
There is no project-scoped credential file, so do not look for one and do not
add one.

Cline reads the repository's `AGENTS.md` natively and lists it in its **Rules**
panel. Keep that rule enabled. No `.clinerules` adapter is needed and this
repository ships none: copying the shared rules into a second file would create a
second owner that drifts.

To verify the instructions are really loaded, check the Rules panel for an
enabled `AGENTS.md` entry, then ask Cline which command verifies this repository.
The answer must be `mise run check`, which appears only in `AGENTS.md`.

To avoid paying a second provider, read the approval header of a request: it
names the provider and model being used. Cline's own usage-billed provider
(Cline provider, ClinePass) is a separate paid path; if a task should run on
DeepSeek, confirm the header says DeepSeek before approving. This repository does
not modify Cline's global configuration.

## Change agent, provider or model later

| Change | Where |
|---|---|
| OpenCode model | `model` in the OpenCode config, `-m` for one run, or `opencode.json` in one project |
| OpenCode provider | Connect that provider's credentials, then set `provider/model` |
| Codex model | `-m`, `-c model=...`, or `model` in a profile file |
| Codex provider or account | User-level `~/.codex/config.toml` and `codex login` |
| Harness | Start a different harness; the shared rules in `AGENTS.md` do not change |
| Role | Your choice per task; nothing routes work automatically |

No model name is a requirement of this repository. `AGENTS.md`, `mise.toml` and
the documentation name identifiers only where a verified example needs one.

## Next steps

- [Agent configuration reference](../reference/agent-configuration.md) —
  locations, precedence, credential storage and verified capabilities.
- [Why the devkit keeps agent configuration native](../explanation/agent-independence.md)
  — the design reasoning.
- [Troubleshoot agent setup](troubleshoot-agent-setup.md) — missing credentials
  and invalid model selection.
