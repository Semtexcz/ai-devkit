# Continuous integration

Reference for this repository's GitHub Actions workflow: what triggers it, what it
runs, which permissions it has, and what it does not prove. The workflow is the
repository file `.github/workflows/verify.yml`; running the same commands locally is
[Diagnose a failed CI job](../how-to/diagnose-ci-failure.md).

## Triggers

| Event | Ref | Runs |
|---|---|---|
| `push` | branches: `main` only | the `verify` job |
| `pull_request` | base branch `main` only | the `verify` job |

Nothing else runs: there is no scheduled job, no manual release job, no
`workflow_run` and no privileged pull-request trigger. Untrusted pull-request code
runs only through `pull_request`, with the read-only token described below.

## Permissions

```yaml
permissions:
  contents: read
```

The workflow declares the permission at workflow level, no job overrides it, and
no step asks for more. `actions/checkout` runs with `persist-credentials: false`,
so the job's Git configuration holds no credential for later steps.

There are no repository secrets, no environment secrets and no model provider
keys: the pipeline needs the package index and the toolchain archives, nothing
else. It never calls a paid model, never authenticates a coding agent and never
prints a credential.

## Pinned actions and the pinned toolchain

| Action | Pinned commit | Release |
|---|---|---|
| `actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | v7.0.1 |
| `jdx/mise-action` | `f5be966e4a917d54244728e6a5fdcd1d93a35e6c` | v5.2.6 |

Full commit identifiers, not tags or branches: a tag can be moved, a commit cannot.
`tests/test_ci_workflow.py` fails when a reference is not a full commit identifier,
when an action outside the reviewed owners appears, or when the workflow mentions a
secret, a model provider key or a write permission.

`jdx/mise-action` installs the mise release this repository tests, `2026.11.1`, and
is called with `install: false`, so the toolchain installation stays an explicit
command in the log rather than a hidden step. The action's cache is described below.

## Installation and verification steps

The job runs, in this order:

```bash
mise trust                       # mark the reviewed mise.toml as trusted
mise install --locked            # runtimes and CLIs from mise.lock and .mise/locks/
mise exec -- uv sync --locked    # Python development tools from uv.lock
mise run versions                # print the installed tuple
mise run check                   # lock check, examples, specs, strict docs
mise run test-template           # generation and update integration tests
git status --porcelain           # must print nothing
```

Every line after the two installs is the command a developer runs locally; the
workflow does not call a checker directly. The last step is the pipeline's own
guarantee: a successful run leaves the tracked tree unchanged, so anything the
checks generate (`.venv/`, `site/`, tool caches) must be ignored by Git.

`mise trust` is explicit because the job must not depend on whether the hosting
image trusts configuration files on its own.

## Caching

One cache, provided by `jdx/mise-action`, holding the mise binary and its
installed tools. Its key includes a hash of the mise configuration files found from
the working directory upwards, `mise.toml` and `mise.lock` among them, so the cache
invalidates when the reviewed toolchain changes. A cache miss installs exactly the
same tuple, only slower, so a green build never depends on a cache hit.

There is no cache for uv's download cache. The Python tools this repository needs
are a small download, and a second cache would need its own key, its own restore
semantics and its own failure mode for a saving that is a fraction of the
toolchain download. It is not worth the extra moving part.

Nothing user-specific is cached: no credentials, no token, no agent configuration.
The cache holds public tool archives for `linux-x64`.

## What the pipeline proves

`mise run check` reads the repository; `mise run test-template` exercises it. Both
run in the same job, so a change that breaks either one fails the pull request:

| Stage | Proves |
|---|---|
| `mise run versions` | the installed toolchain matches the pinned tuple |
| `mise run check` | `uv.lock` matches `pyproject.toml`; the agent configuration examples parse; every OpenSpec change and specification validates; the documentation site builds with no broken internal link |
| `mise run test-template` | a project can be created, verified, specified, updated and broken in every way the contract names |

The individual assertions of `mise run test-template` are listed in
[Generated project: commands and contents](generated-project.md#verifying-the-overlay-in-this-repository).

## Known limitations

- **Hosted evidence is separate from local checks.** The tests in this repository
  check the workflow's contents, not its behavior on a GitHub-hosted runner. Which
  hosted runs have actually passed is recorded in the
  [v0.1.0 acceptance report](../releases/v0.1.0-acceptance-report.md); a green local
  run is still not evidence about hosted CI.
- **One platform.** `ubuntu-24.04` on x86-64 only, matching `lockfile_platforms` in
  `mise.toml`. macOS, Windows and WSL2 are not covered and not claimed.
- **The job needs the package index.** `mise run test-template` installs a generated
  project's dependencies, so the pipeline is not hermetic and is slower than the
  repository checks alone.
- **No release.** There is no tag, publish, deploy or container step, and no
  repository write permission to make one possible.
- **No agent execution.** The pipeline never runs OpenCode or Codex; only their
  credential-free example configuration is parsed.
- **Caching is not measured.** No cache-hit rate is collected or claimed; the
  workflow is written to be correct with and without a cache.
