# Research: documentation components

Inspected on 2026-11-10. This is proposal evidence, not an installation manifest.
The six actual `SKILL.md` files were read at the commits below; their blob
identities matched the default-branch reads. Linked dependencies were inspected
selectively. Nothing from upstream was installed, invoked or executed.

## Sources and maintenance signals

| Component | Inspected source | Repository head date |
|---|---|---|
| writing-technical-documentation | [ramkumar-r-goml/agent-skills](https://github.com/ramkumar-r-goml/agent-skills/blob/d53c72fa39796c081988e5da152ef787b256be63/skills/writing-technical-documentation/SKILL.md) | 2026-11-06 |
| write | [docker/docs](https://github.com/docker/docs/blob/bee24e71ed35df2b63b227b35222e2a213d4e0b2/.agents/skills/write/SKILL.md) | 2026-11-10 |
| writing-for-agents | [mattpocock/skills](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents/SKILL.md) | 2026-10-31 |
| documentation-review | [canonical/kernel-docs](https://github.com/canonical/kernel-docs/blob/98fd72a63a5986892e7ece85d00d4ae34c6a61fa/.github/skills/documentation-review/SKILL.md) | 2026-10-23 |
| good-docs-audit | [ComposioHQ/composio](https://github.com/ComposioHQ/composio/blob/3de004f2622d3f90be830877d2c7f0fa7639c77d/.agents/skills/good-docs-audit/SKILL.md) | 2026-11-10 |
| documentation-diataxis | [canonical/copilot-collections](https://github.com/canonical/copilot-collections/blob/b33daf853e9df2498edf8ada3ba6d15333ca21bc/skills/documentation-diataxis/SKILL.md) | 2026-11-06 |

Dates describe repository heads, not skill releases, review quality or support
commitments. All seven inspected repositories, including Cezar, reported
`archived: false` through GitHub metadata. Recent activity alone does not prove
long-term maintenance. Source paths and pinned links matter: the Matt Pocock
skill is nested under `skills/productivity/`; Canonical's reusable Diátaxis
component was found in `copilot-collections`, rather than guessed from its name.

## Evaluation

### writing-technical-documentation: preferred Writer reference

Strong fit: repository-first reading, evidence statuses, change-impact mode,
small-edit path, broad document-type references, preservation of existing prose,
command verification and prose pruning. Its roles overlap: writing, audit,
planning, conversion and CI advice are bundled in one skill.

Dependencies include its `references/` tree and five CLI scripts sharing
`scripts/doclib.py`. The inspected inventory and reference-checker sources use
the Python standard library; inventory also uses Git. The reference checker lists
commands without executing them and makes URL requests only with an explicit
option. Export features introduce Pandoc and, for relevant outputs, Typst; they
are outside the MVP. The inventory does not list Zensical in its documentation
tool map, so it cannot replace inspection of this repository's `mise.toml` and
`zensical.toml`.
[Inventory](https://github.com/ramkumar-r-goml/agent-skills/blob/d53c72fa39796c081988e5da152ef787b256be63/skills/writing-technical-documentation/scripts/repo_inventory.py),
[reference checker](https://github.com/ramkumar-r-goml/agent-skills/blob/d53c72fa39796c081988e5da152ef787b256be63/skills/writing-technical-documentation/scripts/verify_refs.py),
[shared helpers](https://github.com/ramkumar-r-goml/agent-skills/blob/d53c72fa39796c081988e5da152ef787b256be63/skills/writing-technical-documentation/scripts/doclib.py).

The root [license](https://github.com/ramkumar-r-goml/agent-skills/blob/d53c72fa39796c081988e5da152ef787b256be63/LICENSE)
is MIT. The [README](https://github.com/ramkumar-r-goml/agent-skills/blob/d53c72fa39796c081988e5da152ef787b256be63/README.md)
describes tests and evaluations; its
[CI configuration](https://github.com/ramkumar-r-goml/agent-skills/blob/d53c72fa39796c081988e5da152ef787b256be63/.github/workflows/ci.yml)
runs unittest on Python 3.11 and 3.14 and installs conversion tools. Those runs were
not reproduced or checked for green status here.

Recommendation: compose selected document-type and evidence-writing references
behind a thin ai-devkit Writer contract. Do not invoke the complete upstream
workflow: it mandates scripts, extra approval for long documents, an external
scratch ledger and a reader-test stage, and can assume permission for actions
outside an individual project's scope. Retain useful methods without importing
all those execution rules. No scripts, export assets or installer in the MVP.

### write: useful prose guidance, unsuitable workflow dependency

Read-before-edit, minimal edits, clear verbs and a canonical home for explanations
are useful. Direct adoption would import issue-derived branching, Git commits and
author attribution, Docker-specific front matter and references to `AGENTS.md`,
`CLAUDE.md`, `STYLE.md` and `COMPONENTS.md`.

Its Claude-specific post-edit hook runs Bash, jq and
`npx --no-install rumdl fmt`; manual validation invokes repository
`scripts/lint.sh` and expects rumdl and Vale.
[Hook source](https://github.com/docker/docs/blob/bee24e71ed35df2b63b227b35222e2a213d4e0b2/.agents/skills/write/scripts/post-edit.sh).
The [root license](https://github.com/docker/docs/blob/bee24e71ed35df2b63b227b35222e2a213d4e0b2/LICENSE)
is Apache-2.0; exact assets and notices need checking before redistribution.
This is a workflow maintained inside Docker's documentation repository, with
corresponding coupling and upgrade cost.

Recommendation: reference its prose guidance when useful. Reject whole-skill
adoption, hooks, Git automation and house metadata. They add no necessary MVP
capability and would conflict with ai-devkit's native ownership boundaries.

### writing-for-agents: preferred agent-facing supplement

Useful for triggered context pointers, separating steps from reference,
progressive disclosure, pruning duplicated meanings and making completion
conditions observable. It is a writing reference, not an evidence-verification
or documentation-impact workflow.

No runtime executable is required by the inspected skill. When authoring skills,
it links to
[SKILL-MECHANICS.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents/SKILL-MECHANICS.md).
Invocation metadata there is harness-specific advice, not a portable requirement.
The inspected
[OpenAI metadata](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents/agents/openai.yaml)
contains display text; it is not needed for explicit reference use.
The [root license](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/LICENSE)
is MIT. A broad skill collection increases unrelated installation surface; pin
only the selected references. No automatic quality evaluation was established.

Recommendation: optional supplement for agent instructions, with local
evidence and safety requirements taking precedence. Pruning must preserve useful
constraints and decision rationale; compact vocabulary must remain understandable.

### documentation-review: inspect for methods, do not adopt its orchestrator

It composes five other skills: `documentation-build`,
`documentation-diataxis`, `documentation-structure`,
`documentation-verify` and `documentation-style`, plus a
[report template](https://github.com/canonical/kernel-docs/blob/98fd72a63a5986892e7ece85d00d4ae34c6a61fa/.github/skills/documentation-review/references/doc-review-report-template.md).
It requires every stage and per-stage checkpoints, stops content analysis on build
failure, and assigns importance by review category rather than demonstrated harm.

The inspected
[build skill](https://github.com/canonical/kernel-docs/blob/98fd72a63a5986892e7ece85d00d4ae34c6a61fa/.github/skills/documentation-build/SKILL.md)
is Sphinx/Make-oriented, cleans output and retries commands; optional targets
include spelling, linkcheck, Vale and accessibility tools. That dependency does
not satisfy a strict read-only Auditor and does not validate Zensical.
The [verification skill](https://github.com/canonical/kernel-docs/blob/98fd72a63a5986892e7ece85d00d4ae34c6a61fa/.github/skills/documentation-verify/SKILL.md)
does use repository evidence and guards against treating a failed search as proof
of absence. Those methods are useful without its full pipeline.

Licensing remains unresolved for the exact skill: root `LICENSE` returned 404,
the inspected root directory had no license file, and
[docs/conf.py](https://github.com/canonical/kernel-docs/blob/98fd72a63a5986892e7ece85d00d4ae34c6a61fa/docs/conf.py)
contains starter-pack CC-BY-SA commentary, not an unambiguous license grant for
`.github/skills/`. Do not infer the skill's terms from the documentation theme
or the separately licensed Canonical collection.

Recommendation: no redistribution or runtime dependency until terms are
established. Use as architectural comparison. The locally maintained orchestration
and report hierarchy would otherwise duplicate responsibilities the MVP keeps
manual and the future orchestrator must own.

### good-docs-audit: optional style lens, insufficient independent audit

Compact report-first workflow with locations and concrete rewrites. It requires
`good-docs-writing`, its `references/style-guide.md`, and its own
[process reference](https://github.com/ComposioHQ/composio/blob/3de004f2622d3f90be830877d2c7f0fa7639c77d/.agents/skills/good-docs-audit/references/audit-process.md).
No executable dependency is specified in those instructions.

It audits voice, not implementation truth. It permits edits when asked, whereas
the proposed Auditor never writes. Its
[style guide](https://github.com/ComposioHQ/composio/blob/3de004f2622d3f90be830877d2c7f0fa7639c77d/.agents/skills/good-docs-writing/references/style-guide.md)
derives examples from Modal and mandates punctuation and product terminology that
would cause stylistic nitpicking in other projects. Its high/medium/low voice
ranking cannot become a technical P0–P3 gate.

The [root license](https://github.com/ComposioHQ/composio/blob/3de004f2622d3f90be830877d2c7f0fa7639c77d/LICENSE)
is MIT; provenance of copied third-party examples must still be checked before
redistribution. The inspected monorepo includes skill validation/routing files in
GitHub search results; no effectiveness or CI success claim follows from that.

Recommendation: optional reference for identifying filler and actionable
rewrites. Do not install it as the Auditor or import its product voice or severity
policy. Preserve the project's terminology.

### documentation-diataxis: preferred narrow classification reference

The Canonical collection supplies a focused classification lens with no required
local executable or sibling skill. It references Diátaxis principles and an
external complex-hierarchies page. It explicitly leaves pass/fail to its caller.

Its final constraints force every page into exactly one quadrant, including
hard-to-fit genres. README sections, ADRs, release notes and agent instructions
need more proportional treatment; its paragraph-length hints are observations,
not defects. Use the classification criteria as reference, not the full skill as
an unconditional policy.

The [root license](https://github.com/canonical/copilot-collections/blob/b33daf853e9df2498edf8ada3ba6d15333ca21bc/LICENSE)
is Apache-2.0. The
[collection README](https://github.com/canonical/copilot-collections/blob/b33daf853e9df2498edf8ada3ba6d15333ca21bc/README.md)
describes a synchronizer with yq/snap assumptions; that distribution mechanism is
not a dependency of this text reference and is excluded.

Recommendation: optional atomic structure reference for Writer and Auditor,
subject to the shared standard's README and genre exceptions. Pin separately from
the Writer supplement; do not adopt the collection synchronizer.

## Cezar evidence and limits

Read [reference.md](https://github.com/open-mercato/cezar/blob/6e0aa49bc77090caf0859f42e9e95f794cc2769e/docs/reference.md)
at `6e0aa49bc77090caf0859f42e9e95f794cc2769e` (head dated
2026-11-10), plus
[graph schema/source](https://github.com/open-mercato/cezar/blob/6e0aa49bc77090caf0859f42e9e95f794cc2769e/packages/cezar/src/workflows/graph.ts),
[graph execution tests](https://github.com/open-mercato/cezar/blob/6e0aa49bc77090caf0859f42e9e95f794cc2769e/packages/cezar/src/workflows/graph-run.test.ts)
and relevant portions of
[run.ts](https://github.com/open-mercato/cezar/blob/6e0aa49bc77090caf0859f42e9e95f794cc2769e/packages/cezar/src/workflows/run.ts).
Native graph agents, verdict ports, conditions, bounded loops, human gates and
persisted run recovery provide plausible integration seams. Graph tests cover
loop exhaustion, verdict branching and explicit session continuation. Omit
continuation for independent review; never resume a Writer session as an Auditor.

There is a concrete enforcement caveat:
[read-only enforcement tests](https://github.com/open-mercato/cezar/blob/6e0aa49bc77090caf0859f42e9e95f794cc2769e/packages/cezar/src/workflows/read-only-enforcement.test.ts)
distinguish ordinary Ask mode from an explicitly enforced manager task. Therefore
Ask mode, a skill prompt or `allowedTools` alone is insufficient evidence of an
immutable audit, especially across backends. The reference also documents
permissive backend defaults. No Cezar installation, paid model run, restart trial
or sandbox escape test was performed. No engine insufficiency has been
demonstrated; the appropriate response is a gated future compatibility pilot,
not an engine extension.

## Selection and supply-chain policy

MVP composition is reference-only: ai-devkit owns small role contracts and the
shared rubric; selected external prose stays upstream. Prefer the evidence and
genre guidance from ramkumar, agent-document guidance from Matt Pocock, and
Canonical's narrow Diátaxis criteria. None is a mandatory executable dependency.
Do not execute the raw six workflows with conflicting instructions and hope a
wrapper silently reconciles them.

Record each chosen component's repository, exact commit, paths, applicable
license and intended use in the future standard's reference table. Reuse a
reviewed local copy if a project already has one, otherwise open the pinned
reference only when needed. Missing optional material reduces optional guidance,
not the mandatory evidence checks; disclose its absence. Never fetch or install
code as a side effect of a documentation task.

MIT and Apache-2.0 labels above are observed license text, not a clearance opinion
for every bundled asset. Before copying any material, review that exact revision,
retain applicable notices and licenses, identify modifications and transitive
files, and obtain maintainer acceptance of unresolved terms. Upgrade one component
at a time, review its diff and rerun the same role trials. No auto-update service,
new lock format, forked checker or whole-library dependency is warranted.

## Research limitations

No skill or Cezar was run, so behavior and maintenance observations are static
source evidence. The full transitive script/asset trees, package distribution,
license history and all release tags were not audited; optional scripts remain
unapproved. GitHub search initially rate-limited one query and some guessed paths
returned 404; all six requested skill files were subsequently located and read.
Unresolved kernel-docs skill licensing excludes it from redistribution. Human
review is still needed before implementing the proposed ownership ADR, selecting
a distribution method beyond inert examples, or adopting any orchestrator.

