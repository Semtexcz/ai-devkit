# Troubleshoot agent setup

Diagnose a missing credential or a rejected model identifier without making a
paid request. Configuration locations and precedence are in the
[agent configuration reference](../reference/agent-configuration.md); the setup
steps are in [Configure coding agents](configure-coding-agents.md).

## Missing authentication

| Symptom | Cause | Fix |
|---|---|---|
| `Provider not found: deepseek` from `opencode models deepseek` | That shell has no DeepSeek credential | Complete `/connect` (or `opencode auth login`), or export `DEEPSEEK_API_KEY` in this shell; `opencode auth list` shows whether a credential is stored |
| OpenCode answers with a model you did not select | `model` is unset in the effective config, or `-m` selected another one | Compare `opencode debug config` with what you expect |
| Codex reports `401 Unauthorized` and retries | No ChatGPT login in this `CODEX_HOME` | Run `codex login`, then confirm with `codex login status` |
| `codex login status` reports an API key but you expect a subscription | `codex login --with-api-key` was run, or `OPENAI_API_KEY` is exported | `codex logout`, unset the variable, run `codex login` again |
| Cline answers with another provider | The provider or model dropdown is not DeepSeek | Check the approval header, which names the provider and model |

None of these states requires a working credential to diagnose: every command in
the table reads configuration or local credential state, and none sends a
request.

## Invalid or unavailable model

| Symptom | Cause | Fix |
|---|---|---|
| `Provider not found: <provider>` | The provider has no credential in this shell, so none of its models exist | Authenticate that provider first |
| OpenCode rejects the whole config file | `opencode.json` is not valid JSON or JSONC; the error names the file and position | Fix the syntax; `mise run examples-check` parses the shipped examples |
| `Error loading config.toml: unknown variant ...` | A value is not one of the documented options for that key | Replace it with a listed value, for example `approval_policy = "on-request"` |
| Codex rejects the model at request time | The identifier exists in the catalog but your account cannot use it | Omit `model` to use the account default |
| A model identifier stopped working after an upgrade | The harness or the provider renamed it | Run `mise run versions` and re-check the identifiers in the reference |

Three offline checks answer "what does this shell have?", and they are not
interchangeable:

```bash
opencode auth list                # providers with a stored credential
codex debug models | head -c 400  # model slugs bundled with this Codex build
opencode models                   # models of every provider that has a credential
```

`opencode auth list` is the authentication check: it reads the local credential
store, so it answers the question even when nothing is configured yet. `codex
debug models` lists what the installed build knows, not what your account may
use. `opencode models` lists only providers that are usable in this shell, so a
provider without credentials does not appear at all — which is why a missing
provider looks like a missing model. List the catalog only after the credential
check passes, and do not read a model listing as proof of authentication.

## Inspect the effective configuration

Both harnesses can resolve their configuration in a throwaway home directory, so
neither your real settings nor your credentials are involved:

```bash
tmp="$(mktemp -d)"
mkdir -p "$tmp/home/.config/opencode"
cp examples/agents/opencode.json "$tmp/home/.config/opencode/opencode.json"

env HOME="$tmp/home" \
  XDG_CONFIG_HOME="$tmp/home/.config" \
  XDG_DATA_HOME="$tmp/home/.local/share" \
  XDG_STATE_HOME="$tmp/home/.local/state" \
  XDG_CACHE_HOME="$tmp/home/.cache" \
  "$(mise which opencode)" debug config
```

The printed document is the merged result, so a key that is missing there is not
in force. Copy a candidate file into `$tmp/home/.config/opencode/` first to test
it before touching your own configuration; nothing is written outside the
temporary directory.

Call the harness through `$(mise which opencode)` rather than through the `mise`
shim here. A `mise` shim run with a different `HOME` looks for its data directory
in that home, finds no installed tools, and reinstalls the whole pinned toolchain
into the throwaway directory.

For Codex, point `CODEX_HOME` at a temporary directory:

```bash
CODEX_HOME="$(mktemp -d)" codex doctor
```

With no configuration and no credentials, the auth check fails as expected; that
proves the diagnosis path works, not that Codex is broken. `codex doctor` reports
failures in its rows and still exits 0, so read the rows themselves. It also
rejects `--profile`, so a profile can only be checked by copying its keys into
the temporary `config.toml`.

## Escalate instead of retrying

If an implementation task fails twice with the same evidence — a failing test, a
reproducible error, a rejected request — stop and hand the failure to a person
or to an advanced model. Repeating the same economical attempt spends tokens
without adding information.

## Do not do this to unblock a setup

- Do not put an API key in a project file, a tracked `.env`, or a rule file.
- Do not copy `auth.json` or `providers.json` between machines or harnesses.
- Do not add `--dangerously-bypass-approvals-and-sandbox`, or raise an approval
  policy to `never` outside an already sandboxed environment, to get past a
  prompt.
- Do not delete a checksum, lower a lockfile, or downgrade a harness version to
  make a configuration file load.
