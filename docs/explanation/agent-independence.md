# Why the devkit keeps agent configuration native

[ADR 0001](decisions/0001-minimal-devkit.md) records the decision that each
harness owns its own model, permission and credential configuration. This page
explains the reasoning you need when the setup behaves unexpectedly, and what
would have to change for the devkit to take a different approach.

## The alternative that was rejected

The known alternative, `_ai_project_template`, resolves model choice, permission
policy and context through its own policy layer. That layer is production code:
it has to track every harness's configuration format, every provider's model
names and every release that changes either.

A devkit that added the same layer would own that churn permanently, and the
shared engineering rules would stop being portable: they would describe a
routing schema instead of how to build and verify software.

So the devkit owns only what no harness can own for it — short engineering
rules, decision records, and the documentation of how to configure the harnesses
it recommends.

## One owner per concern

| Concern | Owner | Why not the devkit |
|---|---|---|
| Model, reasoning and permission settings | The harness | Only the harness knows which keys it honours |
| Credentials | The harness's own store | Copying secrets between stores multiplies exposure |
| Which role runs now | The person starting the harness | A role is a judgement about the task, not a setting |
| Shared engineering rules | This repository, as `AGENTS.md` | All three harnesses read it natively |
| Coordination between runs | Nothing, in v0.1 | Orchestration is a product, not a configuration file |

Because the harness owns its configuration, an upstream release that renames a
model or moves a key is an upstream change to document, not a devkit bug to
patch in code.

## Why subscription and API authentication stay separate

ChatGPT subscription access and API-key access are different products:

- they authenticate differently — a browser or device sign-in versus a key;
- they bill differently — a plan with account-dependent limits versus metered
  tokens;
- they are authorized differently — workspace roles and retention settings
  versus API organization settings;
- their credentials are not interchangeable, and neither is a format the other
  harness can consume.

A helper that "just made it work" by falling back from one to the other would
silently change what a task costs and which data-handling policy applies. That is
why the documentation always names the authentication path explicitly, why the
Codex profile ships without a model, and why no example contains a key.

## How the cost-conscious strategy works

The initial split follows from what each kind of work needs:

| Work | Configuration | Reason |
|---|---|---|
| Bounded implementation and repair | Economical model through OpenCode or Cline | The task is specified; output is verifiable by checks |
| Planning, difficult debugging, review | Advanced model through Codex | Judgement matters more than throughput |
| Anything still failing after two attempts | A person or an advanced model | Repeating the same attempt buys no information |

This is a documented operating rule, not an engine. Nothing measures a failure
and escalates automatically, because that would require the devkit to know
per-account limits and per-request prices — knowledge it does not own and cannot
keep current.

Two consequences are stated rather than estimated. DeepSeek usage is metered.
Codex subscription usage has account-dependent limits and is not unlimited. The
documentation never converts one into invented currency figures.

## Why future flexibility survives

- `AGENTS.md` is the only shared artifact a harness must read, and it names no
  model, provider or vendor-specific command.
- Model identifiers appear only in replaceable examples and in a reference table
  that records how each was verified.
- Adding a harness means documenting its configuration locations and adding one
  example; no shared rule changes.
- Removing a harness means deleting its example and its rows. The engineering
  rules are unaffected.

What would break this: a harness that cannot read `AGENTS.md` in any form, or a
capability the devkit needs that no native setting exposes. Either would be a
reason to extend the documentation, and only then to consider code.

## What v0.1 deliberately does not build

No common agent schema, no execution launcher, no model router, no SDK
abstraction, no workflow engine, no credential manager and no automatic
escalation. Selecting a role, or changing a model, is a manual operation
performed with the harness's own configuration.

Automatic role-based routing is deferred, not abandoned. If it is ever added, it
should be an established external tool that invokes the harnesses through these
same native boundaries — not a new layer inside the devkit.
