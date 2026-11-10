# documentation-standard Spec Delta

## Purpose

Provide one reusable, proportional documentation rubric that preserves project
ownership and governs both documentation authoring and independent auditing.

## ADDED Requirements

### Requirement: Both roles use one explicit rubric

Writer and Auditor SHALL use the same identified documentation standard and
project rules. Material conflicts SHALL be reported for human resolution before
the affected action proceeds. External advice SHALL NOT silently override either.

#### Scenario: Conflicting guidance

- **WHEN** an external skill demands metadata absent from the project's conventions
- **THEN** both roles follow the shared project rubric and disclose the external mismatch rather than introducing that metadata or reporting its absence as a defect

#### Scenario: Unresolved project conflict

- **WHEN** an approved project exception conflicts materially with the reusable role contract
- **THEN** the role reports the conflict and stops the affected action pending a human decision

### Requirement: Documentation organization is proportional

The standard SHALL organize information by audience and reader task, apply
Diátaxis where appropriate, define clear document responsibilities and use
progressive disclosure. It SHALL NOT require a directory tree, site generator,
empty document categories or arbitrary document splitting.

#### Scenario: README-only repository

- **WHEN** a small repository serves its readers with README sections
- **THEN** adoption preserves that structure and does not require four Diátaxis directories or additional empty pages

#### Scenario: Larger documentation set

- **WHEN** a project has distinct learning, task, lookup and explanation needs
- **THEN** the standard supports distinct responsibilities and descriptive links in the project's existing structure, while allowing README, ADR and changelog genre exceptions

### Requirement: Facts and lifecycle have authoritative owners

The standard SHALL distinguish source-backed implementation, specified intent,
inference and planned functionality; define canonical sources and links; preserve
ADR history; and require documentation impact assessment during development.
Generated content SHALL retain its existing generator as owner.

#### Scenario: Planned feature

- **WHEN** a feature appears in an approved specification but is absent from implementation
- **THEN** documentation describes it as planned and does not claim it is available

#### Scenario: Changed architectural decision

- **WHEN** a significant accepted decision changes
- **THEN** the project follows its ADR conventions for status, date, context, decision, consequences and alternatives, linking superseding decisions and retaining useful history

#### Scenario: Documentation maintenance

- **WHEN** a public interface or user workflow changes or is retired
- **THEN** its existing maintainer/reviewer owns the same-change documentation assessment, canonical references and affected inbound links without a new ownership database

### Requirement: Agent documentation preserves high-value constraints

Agent-facing documentation SHALL keep essential scope, safety, authority and
completion constraints, use conditional pointers for specialized reference and
avoid duplicated rules, inventories and low-information text. Style observations
SHALL require demonstrated reader impact rather than preferences or AI attribution.

#### Scenario: Concision pass

- **WHEN** repeated policy is removed from agent instructions
- **THEN** a clear pointer retains access to the canonical policy and essential authority and completion constraints remain available

#### Scenario: Subjective style

- **WHEN** prose differs in punctuation but remains clear and technically correct
- **THEN** neither role reports a defect solely for that preference or asserts that the text was AI-generated

### Requirement: External components remain optional and replaceable

External references SHALL identify repository, exact revision, selected paths,
license evidence and intended use. Their execution workflows SHALL NOT be
implicitly invoked. Adoption SHALL preserve upstream ownership and project rules
without automatic installation, synchronization or a mandatory external runtime.

#### Scenario: Optional reference unavailable

- **WHEN** an upstream reference cannot be accessed
- **THEN** the role discloses the limitation and can perform the mandatory local contract without installing a replacement or skipping evidence checks

#### Scenario: Redistribution or upgrade

- **WHEN** a selected component is copied or upgraded
- **THEN** the exact files, transitive dependencies, terms and notices are reviewed and the role trials are repeated before claiming compatibility

#### Scenario: Ownership of reusable guidance

- **WHEN** a project adopts a role example
- **THEN** reusable policy remains identified separately from project-owned documentation, with no edits to OpenSpec-generated integrations or copying of ai-devkit's product plans
