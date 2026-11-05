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
  read by any tool until you copy them, or their settings, to the location named
  below.

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

1. Look before you write. OpenCode 1.19.5 reads
   `~/.config/opencode/opencode.json` or `opencode.jsonc`, and creates
   `opencode.jsonc` the first time it runs.

   ```bash
   ls -a ~/.config/opencode
   ```

   | What you find | What to do |
   |---|---|
   | No file, or no directory | `mkdir -p ~/.config/opencode` and `cp examples/agents/opencode.json ~/.config/opencode/opencode.json` |
   | `opencode.json` exists | Add the two keys to it by hand; keep every other key |
   | `opencode.jsonc` exists | Add the two keys to that file; `.jsonc` wins over `.json` for conflicting keys, so keys added only to a sibling `opencode.json` would have no effect |

   Merging means inserting two members into the object that is already there.
   OpenCode's own first run writes just `{"$schema": ...}`, so that is the
   smallest realistic result:

   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "model": "deepseek/deepseek-flash",
     "small_model": "deepseek/deepseek-flash"
   }
   ```

   Keep whatever else the file already contains. JSON has no trailing commas, so
   a member appended after the last one needs a comma on the line above. If both
   files exist, edit the `.jsonc` one.

   This guide never overwrites an existing OpenCode configuration file. When in
   doubt, add the two keys by hand instead of copying.

   Editing the user file respects OpenCode's merge order instead of fighting it:
   the user file is the default for every project, a project `opencode.json`
   overrides only the keys it names, and `OPENCODE_CONFIG` or
   `OPENCODE_CONFIG_CONTENT`, if you export them, outrank the user file. Do not
   set either variable to force a choice. The full order is in the
   [agent configuration reference](../reference/agent-configuration.md).

2. Authenticate. Inside the OpenCode interface use `/connect`, or log in from the
   shell:

   ```bash
   opencode auth login
   ```

   `auth` is the command name in 1.19.5; `providers` is an alias for the same
   command. Add `--provider deepseek` to skip the provider picker. The key is
   stored in `~/.local/share/opencode/auth.json`, not in your config file. As an
   alternative, export `DEEPSEEK_API_KEY` and OpenCode reads it from the
   environment.

3. Check the credential and the model catalog separately, because they answer
   different questions and either can fail on its own:

   ```bash
   opencode auth list        # which providers have a stored credential
   opencode models deepseek  # which model identifiers this build resolves
   ```

   `opencode auth list` is the authentication check. It reads the local
   credential store and names the file it uses together with the providers
   configured in it; it sends no request. `opencode models deepseek` is the
   catalog check and prints the identifiers:

   ```text
   deepseek/deepseek-flash
   deepseek/deepseek-v4-pro
   ```

   That is the expected output once a DeepSeek credential is present. A model
   list is not an authentication check: in this release a provider appears only
   when a credential for it exists, so `Provider not found: deepseek` means "no
   DeepSeek credential in this shell" — either `opencode auth login` did not
   complete, or `DEEPSEEK_API_KEY` is not exported here.

4. Confirm what is actually in force:

   ```bash
   opencode debug config
   ```

   The document it prints is the merged result, so `"model":
   "deepseek/deepseek-flash"` and `"small_model": "deepseek/deepseek-flash"` must
   appear in it; a key missing there is not in force. To test a candidate file
   before touching your own configuration, use the throwaway-home recipe in
   [Troubleshoot agent setup](troubleshoot-agent-setup.md).

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
ls ~/.codex/ai-devkit-advanced.config.toml   # "No such file" is the normal case
mkdir -p ~/.codex
cp examples/agents/codex/ai-devkit-advanced.config.toml \
  ~/.codex/ai-devkit-advanced.config.toml

codex --profile ai-devkit-advanced
codex exec --profile ai-devkit-advanced "review the current diff"
```

Do not copy over a profile that already exists: edit the existing file instead.
Because a profile is layered over `~/.codex/config.toml`, it only needs the keys
that differ.

A profile is a separate file next to the user config, holding top-level keys
that are layered over `~/.codex/config.toml`. Since Codex 0.134.0 the
`[profiles.<name>]` table and the `profile = "..."` selector are no longer read,
so an existing `~/.codex/config.toml` needs no edit. `--profile` applies to
runtime commands only; `codex doctor` and `codex debug` reject it.

The example sets `approval_policy = "on-request"` and
`sandbox_mode = "workspace-write"`. It deliberately sets no `model`: available
models depend on your account, so the account-supported default stays in effect.

The pinned release accepts both keys: with them placed in a temporary
`CODEX_HOME/config.toml`, `codex doctor` reports `config loaded` and
`approval OnRequest`. `codex doctor` exits 0 even when a check fails, so read its
`Configuration` rows rather than the exit status. Profile resolution itself is
exercised only by runtime commands, which need a signed-in account, so it stays
documented here rather than separately validated.

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
