# Codex Migration Inventory

This document tracks the migration of Cursor-specific agent configuration into the accepted Codex-native repository
structure defined by [ADR-0001](decisions/0001-adopt-codex-native-agent-configuration.md).

The inventory prevents silent rule loss and preserves the parity evidence used before the legacy sources were removed.
All applicable entries were verified, and the user separately approved removal on 2026-09-01.

## Status Definitions

| Status | Meaning |
| :--- | :--- |
| **Migrated** | Normative behavior has a Codex-native destination and was included in parity verification. |
| **Consolidated** | Behavior already exists in, or was intentionally combined into, another authoritative destination. |
| **Pending** | The Cursor source remains authoritative during the transition; Codex-native migration is unfinished. |
| **Conditional** | Migration depends on explicit project adoption or a later project decision. |
| **Incompatible** | No direct Codex equivalent exists; the replacement or limitation must be documented before removal. |
| **Ignored generated artifact** | Generated or cached content has no normative behavior to migrate and must not be committed. |

## Migration Inventory

| Cursor source | Role or classification | Codex-native destination | Status | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `.cursor/README.md` | Cursor customization overview | `docs/project/agent-configuration.md`, `.agents/README.md`, and this inventory | **Consolidated** | Active repository guidance now describes the Codex-native configuration and Skill workflows. Cursor-only metadata, commands, packaging, and troubleshooting details are historical implementation material and are not reproduced as current guidance. |
| `.cursor/agents/reviewer.md` | Independent reviewer definition | `.codex/agents/reviewer.toml` | **Migrated** | Review scope, evidence, severity, output, and report-only behavior are preserved. `sandbox_mode = "read-only"` is an agent default that a parent runtime override can supersede; the instructions independently prohibit repository changes. Cursor's `is_background` metadata has no custom-agent field, so return-to-parent behavior is preserved in the instructions. |
| `.cursor/hooks.json` | Cursor hook registration | `AGENTS.md` and Codex-native sandbox and approval flow | **Incompatible** | The Cursor `beforeShellExecution` registration is not copied. Codex `PreToolUse` does not support the guard's `ask` result, and `PermissionRequest` cannot turn an otherwise unprompted command into an approval request. |
| `.cursor/hooks/shell-guard.py` | Deterministic shell guard | `AGENTS.md` and Codex-native sandbox and approval flow | **Incompatible** | The guard only allows commands or requests approval; it never permanently denies them. Mapping `ask` to `deny` would strengthen policy, while mapping it to `allow` would remove the safety behavior. Approval categories remain governed by `AGENTS.md`; no misleading Codex hook is created. |
| `.cursor/hooks/__pycache__/shell-guard.cpython-314.pyc` | Python bytecode cache | None | **Ignored generated artifact** | Ignored cache with no source semantics. |
| `.cursor/rules/README.md` | Classification, precedence, application modes, navigation | `engineering-standards/SKILL.md`, `references/governance.md`, and this inventory | **Consolidated** | Normative routing and governance were preserved; Cursor-only application-mode terminology is represented as skill routing. |
| `.cursor/rules/meta/README.md` | Meta-rule navigation and classification | `engineering-standards/SKILL.md` and this inventory | **Consolidated** | All listed meta rules have explicit destinations below. |
| `.cursor/rules/meta/compatibility.mdc` | HYBRID; always applicable | `references/governance.md` | **Migrated** | Version authority and reviewed baselines preserved. |
| `.cursor/rules/meta/compliance.mdc` | GENERAL; always applicable | `references/governance.md` | **Migrated** | Scope, precedence, conflict, proportionality, and exception semantics preserved. |
| `.cursor/rules/meta/git-workflow.mdc` | GENERAL; always applicable | `references/git-workflow.md` | **Migrated** | Branch-source and temporary-dependency rules preserved. |
| `.cursor/rules/meta/markdown.mdc` | HYBRID; Markdown files | `references/documentation.md` | **Migrated** | Mechanical style, documentation quality, Mermaid, and table guidance preserved. |
| `.cursor/rules/meta/workflow.mdc` | REUSABLE PROJECT BASELINE; always applicable | `AGENTS.md` | **Consolidated** | The root working agreement is already the more complete authority for planning, approval, scope, implementation, and replanning. |
| `.cursor/rules/repository/README.md` | Repository-rule navigation and opt-in boundaries | `engineering-standards/SKILL.md` and this inventory | **Consolidated** | Optional status and routing are explicit. |
| `.cursor/rules/repository/branch-discipline.mdc` | REUSABLE PROJECT BASELINE; opt-in | `references/branch-discipline.md` | **Migrated** | Remains inactive unless explicitly adopted. |
| `.cursor/rules/repository/file-authorship.mdc` | REUSABLE PROJECT BASELINE; opt-in | `references/file-authorship.md` | **Migrated** | Remains inactive unless explicitly adopted. |
| `.cursor/rules/python/README.md` | Python-rule navigation and classification | `engineering-standards/SKILL.md` and this inventory | **Consolidated** | Every listed Python rule has an explicit routed destination below. |
| `.cursor/rules/python/conventions.mdc` | PERSONAL CONVENTION; Python files | `references/python-conventions.md` | **Migrated** | Preserved as applicable personal guidance subordinate to authoritative requirements. |
| `.cursor/rules/python/core.mdc` | HYBRID; Python files | `references/python-core.md` | **Migrated** | Change discipline, design, errors, typing, documentation, and validation preserved. |
| `.cursor/rules/python/observability.mdc` | GENERAL; concern-specific | `references/python-observability.md` | **Migrated** | Logging, metrics, tracing, telemetry, and health signaling preserved. |
| `.cursor/rules/python/test-conventions.mdc` | PERSONAL CONVENTION; Python tests | `references/python-test-conventions.md` | **Migrated** | Preserved as applicable personal test guidance subordinate to authoritative requirements. |
| `.cursor/rules/python/tests.mdc` | GENERAL; Python tests | `references/python-tests.md` | **Migrated** | Test quality, isolation, doubles, fixtures, and test portfolio preserved. |
| `.cursor/rules/python/tooling.mdc` | REUSABLE PROJECT BASELINE; concern-specific | `references/python-tooling.md` | **Migrated** | uv, Ruff, Pyright, and Pylance responsibilities preserved. |
| `.cursor/rules/architecture/README.md` | Architecture navigation and classification | `engineering-standards/SKILL.md` and this inventory | **Consolidated** | All eight architecture rules have explicit routed destinations. |
| `.cursor/rules/architecture/application.mdc` | GENERAL; concern-specific | `references/architecture-application.md` | **Migrated** | Services, boundary models, CQRS, read models, and error boundaries preserved. |
| `.cursor/rules/architecture/boundaries-packages.mdc` | GENERAL; concern-specific | `references/architecture-boundaries-packages.md` | **Migrated** | Public seams, context boundaries, dependency assembly, enforcement, and packaging preserved. |
| `.cursor/rules/architecture/concurrency.mdc` | GENERAL; concern-specific | `references/architecture-concurrency.md` | **Migrated** | State ownership, concurrency boundaries, locking, idempotency, caches, and constraints preserved. |
| `.cursor/rules/architecture/construction-strategies.mdc` | GENERAL; concern-specific | `references/architecture-construction-strategies.md` | **Migrated** | Construction, reconstitution, factory, Strategy, Policy, and registry rules preserved. |
| `.cursor/rules/architecture/core.mdc` | GENERAL; Python files | `references/architecture-core.md` | **Migrated** | Anti-ceremony design, dependency direction, and layer responsibilities preserved. |
| `.cursor/rules/architecture/domain-model.mdc` | GENERAL; concern-specific | `references/architecture-domain-model.md` | **Migrated** | Entities, value objects, aggregates, identity, and invariants preserved. |
| `.cursor/rules/architecture/events-workflows.mdc` | GENERAL; concern-specific | `references/architecture-events-workflows.md` | **Migrated** | Events, transactions, outbox, retries, compensation, and distributed workflows preserved. |
| `.cursor/rules/architecture/persistence.mdc` | GENERAL; concern-specific | `references/architecture-persistence.md` | **Migrated** | Repository, query, transaction, and Unit of Work boundaries preserved. |

## Removal Record

The `.cursor/` directory was removed from the working tree on 2026-09-01 after:

1. every normative source received a `Migrated`, `Consolidated`, `Conditional`, or explicitly `Incompatible` outcome
   with a recorded replacement or limitation;
2. migrated behavior passed parity verification;
3. no authoritative link depended on a Cursor source; and
4. the user approved a separate removal batch.

This record does not authorize or imply any Git operation. Staging, committing, and pushing remain separate approval
boundaries.
