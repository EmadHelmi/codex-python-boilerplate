---
name: engineering-standards
description: >-
  Apply this repository's engineering standards while planning, implementing,
  reviewing, or verifying code, tests, documentation, architecture, tooling,
  or Git workflow changes; load only references relevant to the current task.
---

# Engineering Standards

Use this skill to discover and apply repository engineering rules without loading every standard into context.

## Authority

- Follow [`AGENTS.md`](../../../AGENTS.md) for human-agent workflow, approval boundaries, and Git authorization.
- Follow the project definition and applicable accepted ADRs for product requirements and accepted technical decisions.
- Treat the references in this skill as reusable engineering standards, not as permission to expand scope or mutate the
  repository.

## Reference Routing

Read only the references that apply to the current work:

| When the task concerns | Read |
| :--- | :--- |
| Rule applicability, precedence, conflicts, or version-sensitive guidance | [`references/governance.md`](references/governance.md) |
| Markdown or repository documentation | [`references/documentation.md`](references/documentation.md) |
| Selecting the source branch or managing dependent branches | [`references/git-workflow.md`](references/git-workflow.md) |
| Strict issue-numbered branch policy explicitly adopted by a repository | [`references/branch-discipline.md`](references/branch-discipline.md) |
| Per-file authorship explicitly adopted by a repository | [`references/file-authorship.md`](references/file-authorship.md) |
| Python implementation, including Python tests | [`references/python-core.md`](references/python-core.md), [`references/python-conventions.md`](references/python-conventions.md), and [`references/architecture-core.md`](references/architecture-core.md) |
| Python dependencies, environments, linting, formatting, or type-checking tools | [`references/python-tooling.md`](references/python-tooling.md) |
| Python logging, metrics, tracing, telemetry, or health signals | [`references/python-observability.md`](references/python-observability.md) |
| Python test implementation or test strategy | [`references/python-tests.md`](references/python-tests.md) and [`references/python-test-conventions.md`](references/python-test-conventions.md) |
| Package structure, public seams, bounded contexts, dependency assembly, or architecture enforcement | [`references/architecture-boundaries-packages.md`](references/architecture-boundaries-packages.md) |
| Entities, value objects, aggregates, identity, or domain invariants | [`references/architecture-domain-model.md`](references/architecture-domain-model.md) |
| Use cases, services, DTOs, commands, queries, CQRS, read models, or error boundaries | [`references/architecture-application.md`](references/architecture-application.md) |
| Repositories, persistence mapping, aggregate loading, transactions, or Unit of Work | [`references/architecture-persistence.md`](references/architecture-persistence.md) |
| Shared mutable state, concurrent persistence, locks, idempotency, caches, or distributed locks | [`references/architecture-concurrency.md`](references/architecture-concurrency.md) |
| Factories, named constructors, reconstitution, Strategy, Policy, registries, or discriminator-driven behavior | [`references/architecture-construction-strategies.md`](references/architecture-construction-strategies.md) |
| Domain or integration events, outbox, side effects, retries, sagas, or distributed workflows | [`references/architecture-events-workflows.md`](references/architecture-events-workflows.md) |

The branch-discipline and file-authorship references are opt-in profiles. Do not apply them merely because they exist.
Read them when the repository explicitly adopts the profile or when the user asks to evaluate adopting it.

## Application Procedure

1. Identify the files, technologies, and engineering concerns affected by the task.
2. Read `references/governance.md`, then only the additional routed references that apply.
3. Inspect authoritative project configuration when behavior depends on versions, tools, or repository policy.
4. Apply requirements proportionally to the approved scope.
5. Surface material conflicts or missing applicable guidance instead of silently choosing or inventing a rule.
6. During verification, check the changed behavior against the same references used during implementation.

## Precedence

Do not infer authority from filenames, directory order, or where a rule is stored. Apply direct task instructions and
authoritative repository sources according to their declared responsibility. Within engineering standards, prefer a
narrower applicable rule and an explicit repository or organization requirement over a reusable default. Never let a
personal convention override correctness or an authoritative requirement.
