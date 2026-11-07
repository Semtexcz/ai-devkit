# Agent configuration reference

Exact locations, scopes, precedence and credential storage for the three initial
harnesses, plus what has been verified in this repository and what has not.
Procedures are in [Configure coding agents](../how-to/configure-coding-agents.md).

## Concepts and owners

The harness, the provider, the model, the execution profile, the role and an
orchestrator are separate concerns with separate owners.

| Concept | Meaning | Owner |
|---|---|---|
| Harness | The coding application: OpenCode, Codex CLI, Cline | Its own vendor and its own configuration |
| Provider | The API account serving a model: DeepSeek, OpenAI | The harness's credential store |
| Model | A provider-specific identifier selected through the harness | Harness configuration, per run or per profile |
| Execution profile | Native settings for model, reasoning and permissions | Harness configuration files |
| Role | Planner, implementer, reviewer, fixer — a per-task choice | You, when you start a harness |
| Orchestrator | An optional process coordinating runs | Absent in v0.1 |

There is no shared role-to-model schema, because one would duplicate native
configuration and make the shared standards depend on a harness. The reasoning
is in [Why the devkit keeps agent configuration native](../explanation/agent-independence.md).

## Configuration files and scopes

| Harness | User level | Project level | Format |
|---|---|---|---|
| OpenCode 1.19.5 | `~/.config/opencode/opencode.json` | `opencode.json` at the project root, `.opencode/` directories | JSON or JSONC |
| Codex CLI 0.163.0 | `$CODEX_HOME/config.toml` (default `~/.codex/config.toml`), profiles in `$CODEX_HOME/<name>.config.toml` | `.codex/config.toml` in a trusted project | TOML |
| Cline 4.1.26 | `~/.cline/data/settings/providers.json` (credentials), `~/.cline/rules/` | `.cline/rules/`, legacy `.clinerules/`, `AGENTS.md` | Interface-driven for provider and model |

Shared instructions are the exception: `AGENTS.md` at the project root is read
natively by all three, so it has exactly one copy and no per-harness adapter.

## Precedence

Codex resolves values in this order, highest first:

1. CLI flags and `-c`/`--config` overrides.
2. Project `.codex/config.toml`, from the project root towards the working
   directory, closest wins; loaded only for a trusted project.
3. The profile file selected with `-p`/`--profile`.
4. User `$CODEX_HOME/config.toml`.
5. Cloud-managed defaults, then `/etc/codex/config.toml`, then built-in defaults.

Two consequences matter in practice. A project layer outranks a profile, and a
profile outranks the user config, so a profile only needs the values that differ.

OpenCode merges its sources instead of replacing them: settings from all
locations are combined and later sources win only for conflicting keys. The
documented order, last wins, is remote organizational defaults, global config,
`OPENCODE_CONFIG`, project `opencode.json`, `.opencode/` directories,
`OPENCODE_CONFIG_CONTENT`, managed settings. Merging is what makes a project
file additive; here, a project `model` overrides the global one while the global
`small_model` survives.

Two file-level details are worth knowing in the pinned 1.19.5 release. It writes
`~/.config/opencode/opencode.jsonc` on first run, and when `opencode.jsonc` and
`opencode.json` both exist in the same directory, the `.jsonc` file wins for
conflicting keys.

## What project-scoped configuration cannot do

Codex ignores these keys in `.codex/config.toml` and warns at startup:
`openai_base_url`, `chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`,
`model_providers`, `notify`, `profile`, `profiles`,
`experimental_realtime_ws_base_url` and `otel`. Provider, notification,
telemetry and profile selection therefore live in the user config only. An
untrusted project loses its whole `.codex/` layer, including rules and hooks.

Cline keeps provider credentials and model selection in global settings; its
`.cline/` directory carries rules, workflows, skills, hooks, agents and plugins,
not credentials.

OpenCode has no such restriction: any key it supports, including `model`, can
appear in a project `opencode.json`. That is a capability difference between
harnesses, not a devkit policy.

## Model and provider selection

| Mechanism | OpenCode | Codex CLI | Cline |
|---|---|---|---|
| Default from configuration | `model` as `provider/model` | `model` in user config or profile | No file; the selected model in settings |
| Auxiliary model | `small_model` | Not documented | Not documented |
| Per-run override | `--model provider/model` on `opencode` or `opencode run` | `-m <model>`, `-c model=<model>` | Per-task model choice in the interface |
| Interactive switch | `/models` | `/model` in the session | Model dropdown |
| Identifier check | `opencode models [provider]` | `codex debug models` | Model dropdown |
| Credential check | `opencode auth list` | `codex login status` | Provider settings panel |
| Provider selection | Credential plus `provider/model` | `model_provider` in user config | API Provider dropdown |

OpenCode resolves the model to use in this order: the `--model` flag (short form
`-m`), then `model` from the merged config, then the last used model, then an
internal priority.

## Verified identifiers

Recorded with the versions pinned in [Tool ownership and pinned versions](tool-versions.md).

| Where | Identifier | How it was verified |
|---|---|---|
| OpenCode 1.19.5 | `deepseek/deepseek-flash` | `opencode models deepseek` in a credential-present shell |
| OpenCode 1.19.5 | `deepseek/deepseek-v4-pro` | Same listing |
| DeepSeek API | `deepseek-flash` (economical), `deepseek-v4-pro` (advanced) | Provider model and pricing documentation |
| Codex CLI 0.163.0 | Account default; this build reports `gpt-6.1-sol` when `model` is unset | `codex exec` session header |
| Cline 4.1.26 | `deepseek-flash` | Identifier present in the installed extension bundle |

DeepSeek still accepts the legacy `deepseek-v4-flash` and
`deepseek-v4-flash-vision-exp` names, but those models are retired: requests are
served by the current Flash model and billed at the Flash price. Prefer
`deepseek-flash`.

The Codex model slug is not a recommendation. Model availability depends on the
signed-in account, which is why the shipped profile sets no `model` and the
shared engineering rules name none.

## Credential handling

| Harness | Native storage | Environment alternative | Written by |
|---|---|---|---|
| OpenCode | `~/.local/share/opencode/auth.json` | `DEEPSEEK_API_KEY` | `/connect`, `opencode auth login` |
| Codex CLI | `~/.codex/auth.json`, or the OS credential store chosen by `cli_auth_credentials_store` | `OPENAI_API_KEY`, which means API billing | `codex login` |
| Cline | `~/.cline/data/settings/providers.json` | Not documented | The Cline settings interface |

The same rules hold for all three:

- A credential never enters a tracked file, a project configuration file or a
  rule file.
- A credential is never copied between harnesses or machines. Each store is
  authoritative for its own harness.
- `.gitignore` keeps an untracked key out of Git. It is not an access-control
  mechanism and does not stop an agent from reading a file.
- A pinned harness version is reproducible; a credential and a model are not
  artifacts and cannot be locked.

## Billing paths

| Path | Authentication | Billing |
|---|---|---|
| ChatGPT subscription, Codex CLI | `codex login` browser or device flow | Included in the plan, with account-dependent limits |
| DeepSeek API key, OpenCode or Cline | Key in the harness's own store | Metered per token |
| OpenAI API key, Codex CLI | `codex login --with-api-key` | Metered per token |

Subscription access and API access are different products with different
billing. Neither is silently substituted for the other, and subscription usage is
never presented as unlimited.

## Supported and unverified capabilities

`Verified` means the pinned version was exercised in an isolated, credential-free
environment. `Documented` means the vendor documentation states it but this
repository has not measured it.

| Capability | OpenCode 1.19.5 | Codex CLI 0.163.0 | Cline 4.1.26 |
|---|---|---|---|
| Reads `AGENTS.md` from the project root | Documented | Documented | Documented |
| Project config overrides the default model | Verified | Documented | Not supported; the model is global |
| Project config selects a provider or credentials | Allowed by the merge order, unverified | Ignored by design | Not supported |
| Named execution profiles | None; configuration layers instead | Verified | None documented |
| Sandbox modes | Permissions documented, unverified | Verified: `read-only`, `workspace-write`, `danger-full-access` | `CLINE_SANDBOX` documented, unverified |
| Approval prompts | Permissions documented, unverified | Verified for interactive runs; `codex exec` never asks | Auto-approve settings documented, unverified |
| Auxiliary model comes from configuration | Accepted by 1.19.5, runtime effect unverified | Not documented | Not documented |
| Non-interactive run | `opencode run` | `codex exec`, verified to fail closed without credentials | Not covered here |

Explicitly unverified, and not claimed:

- authenticated end-to-end behaviour of any harness — no paid request was made
  while preparing this configuration;
- whether each harness really injects `AGENTS.md` into its context at runtime;
- the exact model list a particular Cline release renders in its dropdown;
- whether `small_model` still influences OpenCode auxiliary calls in a future
  release.

## What this repository deliberately does not configure

- No `opencode.json`, `.codex/`, `.cline/` or `.clinerules` at the repository
  root, so no project-scoped agent configuration is active here.
- No custom provider definitions: `deepseek` is the built-in provider.
- No API keys, tokens or session credentials.
- No launcher, router or role-to-model schema.

## Verification commands

Three layers answer three different questions. Only the first is automated, and
none of them is evidence of an authenticated session.

| Layer | Command | What it proves | Needs credentials |
|---|---|---|---|
| Syntax | `mise run examples-check` | The shipped JSON and TOML examples parse | No |
| CLI configuration | `opencode debug config` and `codex doctor` with a throwaway home | The pinned release loads and accepts the shipped keys | No |
| Authenticated execution | `opencode run "..."`, `codex exec "..."` | A real model request completes and is billed | Yes — not tested here |

`mise run examples-check` deliberately stays a standard-library parse: it is
fast, offline, deterministic and never reads or writes a user configuration.
Starting a harness is a separate manual step, because it creates local state and
may fetch the model catalog.

The throwaway-home recipe for both harnesses is in
[Troubleshoot agent setup](../how-to/troubleshoot-agent-setup.md).

| Command | Reads |
|---|---|
| `mise run examples-check` | The example files in this repository |
| `mise run versions` | The installed harness versions, for comparison with the pins |
| `opencode auth list` | The local credential store and the providers configured in it |
| `opencode models [provider]` | The model catalog the build resolves; a provider appears only when it has a credential |
| `opencode debug config` | The merged OpenCode configuration for the current directory |
| `codex login status` | Which Codex authentication method is active |
| `codex doctor` | Codex configuration, authentication and runtime state |

All of these read configuration or local state and send no model request. Codex
Doctor reports a failing check in its rows and still exits 0, so read the rows
rather than the exit status. See
[Troubleshoot agent setup](../how-to/troubleshoot-agent-setup.md) for isolated
diagnosis.
