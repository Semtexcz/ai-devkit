# Tasks

Planning only: none of these implementation tasks is authorized or completed by
creating this proposal. Apply only after explicit human approval. Scope is the
manual MVP; Cezar configuration, installed distribution, new CI checks, overlay
changes and external code installation are deferred to separate changes.

## 1. Establish the shared documentation contract

- [ ] 1.1 Record the next numbered ownership ADR for inert role examples and optional upstream references; verify it preserves the vision's owners and links to ADR 0001 without changing OpenSpec-generated directories.
- [ ] 1.2 Write `docs/reference/documentation-standard.md` from the standard spec and design rubric; verify its rules work for both a README-only fixture and the existing docs tree, including genre exceptions and P0–P3/PASS/FAIL/INCOMPLETE meanings.
- [ ] 1.3 Add the selected upstream reference table to that standard with immutable revisions, exact paths, intended use and license evidence from `research.md`; verify every selected dependency is optional, no executable is imported and kernel-docs remains excluded from redistribution pending explicit terms.

## 2. Deliver opt-in roles and their manual procedure

- [ ] 2.1 Create `examples/skills/README.md` explaining explicit invocation, shared-standard links, isolation and the OpenSpec ownership boundary; verify links resolve from the example location and no install, symlink or global configuration change is required.
- [ ] 2.2 Add the inert Documentation Writer `SKILL.md` example linking to the standard; verify a small fixture invocation returns an evidenced impact decision, minimal edit or no-op and complete verification limits without running upstream tools.
- [ ] 2.3 Add the separate inert Documentation Auditor `SKILL.md` example linking to the same standard; verify a fresh read-only session returns a complete finding and verdict on one planted stale claim while the fixture content remains unchanged.
- [ ] 2.4 Write `docs/how-to/write-and-audit-documentation.md` with standalone role prompts, the manual handoff, candidate binding, shared two-attempt bound and failure paths; verify a reader can identify who runs checks, who saves reports and when to escalate without a second tracker.

## 3. Validate the integrated manual workflow

- [ ] 3.1 Run Writer assessment then independent Auditor on a README-only internal-refactor fixture; verify both support no-update with source evidence and no documentation churn.
- [ ] 3.2 Run the workflow on a fixture with a changed CLI flag/default and initially untouched docs; verify the impact decision identifies the correct documents, Writer makes only necessary edits and Auditor independently verifies the new behavior.
- [ ] 3.3 Exercise the role contracts on README, architecture, API reference, CLI reference, tutorial, how-to, ADR and agent-instruction examples; verify genre-appropriate guidance and retention of useful existing content without mandatory companion pages.
- [ ] 3.4 Audit a mixed fixture containing stale facts, a missing prerequisite, contradiction, duplication, broken link, invalid command and obstructive filler; verify every planted blocking defect has evidence, no unsupported confirmed blocker appears, report fields are complete and PASS/FAIL/INCOMPLETE plus P0 escalation behave as designed.
- [ ] 3.5 Run the Auditor in a fresh immutable environment against the integrated fixture; verify a deliberate write is denied, before/after snapshots outside the repository show no changed/created/deleted repository content and no Writer session context was supplied.
- [ ] 3.6 Walk conflict, unavailable-evidence, optional-reference failure and two unsuccessful repair paths; verify exact finding transfer, no third repair, no multiplied retry allowance and fresh final review/check evidence after head changes. Record outcomes and limitations in the existing review record, without a new state file.

## 4. Integrate discovery and complete repository verification

- [ ] 4.1 Add navigation and short discovery links in `zensical.toml`, the documentation index and `AGENTS.md`; add the implemented capability under `[Unreleased]` in `CHANGELOG.md`; verify links target canonical material and descriptions claim only the manual behavior actually trialed.
- [ ] 4.2 Run `mise exec -- openspec validate add-documentation-workflow --strict --no-interactive` and `mise run check`; verify all pass, review the cross-artifact acceptance matrix and diff, and confirm checks changed no tracked source or generated integrations.
- [ ] 4.3 Prepare the existing evidence-bound handoff with trial results, exact candidate commits, independent review, changelog decision and limitations; verify no Cezar adoption, engine extension, CI model call, overlay modification or installation was introduced and all consequential actions remain pending human authorization.

## Workflow follow-up

- Archive only after implementation, independent review and the project's human approval requirements are satisfied, using the native OpenSpec workflow.
- Propose Level 2 only after choosing an orchestrator and demonstrating isolation, bounded retries and restart recovery on a pinned release; keep run state with that orchestrator.
- Propose Level 3 additions only for demonstrated deterministic coverage gaps; reuse maintained checkers and preserve the existing CI permission and credential contract.
