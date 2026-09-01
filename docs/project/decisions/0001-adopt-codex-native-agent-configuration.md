# ADR-0001: Adopt Codex-Native Agent Configuration

- Status: `Accepted`
- Date: 2026-08-31

## Context

The repository was initialized with a substantial Cursor-specific integration
layer. Its engineering guidance is stored in `.cursor/rules/`, its independent
reviewer is defined in `.cursor/agents/`, and its command guard uses Cursor's
hook schema under `.cursor/hooks/`.

The project will use Codex as its repository agent. Cursor Project Rules,
Cursor subagent frontmatter, and Cursor hook events are not Codex-native
interfaces. Copying those files without conversion would leave important
guidance undiscoverable or give it different runtime semantics.

The existing rule set is valuable and must remain available. It includes
governance, repository, Python, testing, observability, and architecture
guidance, including explicitly classified personal conventions and optional
profiles. Loading all of that material into `AGENTS.md` would also be
inappropriate: the file is already close to Codex's default project-instruction
size limit, and unrelated rules would consume context on every task.

## Decision Drivers

- Make all repository agent configuration understandable and usable by Codex.
- Preserve the meaning, scope, classification, and precedence of every existing
  engineering rule.
- Keep one canonical source for each instruction to avoid configuration drift.
- Load detailed guidance only when it is relevant to the current work.
- Preserve explicit human approval and Git-operation boundaries.
- Avoid pretending that superficially similar Cursor and Codex mechanisms have
  identical behavior.
- Keep the resulting configuration reviewable and maintainable.

## Decision

The repository will adopt a Codex-native agent configuration and will not
maintain a parallel Cursor integration after migration is verified.

The migration will follow these rules:

1. `AGENTS.md` remains the authoritative human-agent working agreement. It will
   be made concise and will route agents to specialized guidance instead of
   duplicating that guidance.
2. Existing workflow skills remain under `.agents/skills/`, which Codex supports
   as a repository skill location.
3. Engineering rules currently stored as Cursor `.mdc` files will move into a
   dedicated `engineering-standards` skill. Its `SKILL.md` will define an
   applicability and routing table, while focused files under `references/`
   will preserve the detailed standards.
4. `AGENTS.md` will require use of the engineering-standards skill before
   relevant code, test, documentation, architecture, or repository changes.
5. Cursor `alwaysApply`, `globs`, and intelligent-application metadata will be
   translated into explicit Codex routing conditions. They will not be copied
   as unsupported metadata.
6. Personal conventions and optional profiles will remain clearly classified.
   Migration will preserve their adopted or conditional status rather than
   silently strengthening or weakening them.
7. The independent reviewer will be converted to a project-scoped Codex custom
   agent under `.codex/agents/` with read-only sandbox intent.
8. Cursor's `beforeShellExecution` hook will not be copied directly. Its `ask`
   behavior does not have equivalent `PreToolUse` semantics in Codex. Approval
   boundaries will remain authoritative in `AGENTS.md` and will use Codex's
   native sandbox and approval mechanisms. A Codex hook or command rule may be
   added later only when its enforceable behavior is explicit and accurate.
9. Codex `.rules` files will not be used as a home for engineering guidance;
   they are reserved for Codex command-execution policy.
10. Every Cursor-specific file will be included in a migration inventory. It
    must be classified as migrated, consolidated without semantic loss,
    intentionally conditional, or incompatible with an explicit explanation.
11. `.cursor/` will be removed only after the migration inventory and parity
    review confirm that no required instruction was silently lost.

All repository documentation produced by this project will be written in
English unless the user explicitly requests otherwise for a specific section.

## Consequences

### Positive

- Codex can discover the repository's workflows and specialized guidance
  through native mechanisms.
- Detailed rules remain available without crowding every task's initial
  context.
- A single canonical configuration avoids Cursor/Codex drift.
- Migration parity is reviewable before Cursor-specific files are removed.
- Unsupported hook behavior is not represented as if it were enforceable.

### Negative

- Cursor-specific configuration will no longer be maintained after migration.
- The migration requires careful classification and parity verification rather
  than a mechanical file rename.
- Correct rule application depends on accurate skill descriptions, routing,
  and the mandatory routing instruction in `AGENTS.md`.
- Contributors who use Cursor will not receive repository-native Cursor Rules,
  subagents, or hooks after the migration.

## Alternatives Considered

### Maintain Native Integrations for Both Codex and Cursor

Shared guidance could be combined with separate thin adapters for both tools.
This would retain first-class support for both agents, but it would add ongoing
maintenance and a material risk that applicability or runtime behavior would
drift between adapters. The project does not currently require dual-agent
support.

### Keep Cursor Configuration and Add Duplicated Codex Files

This would minimize the initial conversion effort, but it would create two
sources of truth and make future rule changes easy to apply inconsistently. It
was rejected because it conflicts with the maintainability and explicit-source
requirements of the repository.

### Put Every Engineering Rule in `AGENTS.md`

This would make the rules immediately visible but would exceed a practical
instruction budget, load unrelated guidance for every task, and duplicate
responsibilities already assigned to specialized engineering standards. It was
rejected in favor of progressive disclosure.

## References

- [`AGENTS.md`](../../../AGENTS.md)
- [Architecture Decision Record policy](README.md)
- [ADR template](template.md)
- [Codex custom instructions with `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
