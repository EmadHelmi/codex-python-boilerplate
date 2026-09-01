# Repository Agent Configuration

This document explains the repository's Codex-native agent configuration and
where each kind of instruction belongs.

It is a navigation and maintenance guide. It does not replace the authoritative
working agreement, project definition, accepted decisions, or engineering
standards that it links to.

## Configuration Map

```text
AGENTS.md
.agents/
└── skills/
    ├── engineering-standards/
    ├── implement-approved-batch/
    ├── project-bootstrap/
    ├── technical-decision/
    └── verify-change/
.codex/
└── agents/
    └── reviewer.toml
docs/project/
├── agent-configuration.md
├── codex-migration-inventory.md
├── definition.md
└── decisions/
```

`docs/project/definition.md` is the designated project-definition location. It
may not exist during repository initialization, but project implementation must
not invent requirements in its absence.

## Sources of Truth

| Source | Responsibility |
| :--- | :--- |
| [`AGENTS.md`](../../AGENTS.md) | Human-agent workflow, approval boundaries, scope control, review, and Git authorization |
| [Engineering standards](../../.agents/skills/engineering-standards/SKILL.md) | Routing to applicable coding, testing, architecture, tooling, documentation, and repository standards |
| [Workflow Skills](../../.agents/README.md) | Reusable procedures for bootstrap, decisions, approved implementation, and verification |
| `docs/project/definition.md` (when created) | Product goals, scope, requirements, constraints, and definition of done |
| [Accepted ADRs](decisions/README.md) | Meaningful technical and architectural decisions already accepted by the user |
| [Reviewer](../../.codex/agents/reviewer.toml) | Optional independent, report-only review after verification |
| [Migration inventory](codex-migration-inventory.md) | Historical parity evidence for the Cursor-to-Codex conversion |

Do not duplicate a normative rule across these sources. Link to its owner when
another document needs to explain where the rule comes from.

## Choosing the Right Mechanism

| Need | Mechanism |
| :--- | :---: |
| Control how agents discuss, decide, implement, verify, and use Git | `AGENTS.md` |
| Provide reusable engineering guidance only when relevant | Engineering-standards Skill and focused references |
| Provide a reusable multi-step procedure | Workflow Skill |
| Provide an independent specialist with separate instructions | Custom agent under `.codex/agents/` |
| Enforce or automate a supported lifecycle event | Codex hook, only when its runtime semantics are explicit |
| Record project requirements | `docs/project/definition.md` |
| Preserve an accepted meaningful technical decision | ADR under `docs/project/decisions/` |

Choose the narrowest mechanism that owns the concern. A convenient duplicate
is still a second source of truth and can drift.

## Working Agreement

[`AGENTS.md`](../../AGENTS.md) is the authoritative behavioral contract for
agents in this repository. It defines the human-controlled lifecycle:

```text
DISCUSS
→ DECIDE
→ RECORD DECISION
→ PLAN
→ USER APPROVAL
→ IMPLEMENT
→ VERIFY
→ USER REVIEW
→ COMMIT APPROVAL
```

These boundaries remain distinct. In particular, implementation approval does
not authorize a commit, and a successful verification result does not authorize
the next batch.

## Skills and Engineering Standards

Repository Skills live under `.agents/skills/`. Their frontmatter describes
when Codex should load them, while their bodies define focused procedures.

The `engineering-standards` Skill uses progressive disclosure: its routing
table selects only the references relevant to the current task. This keeps
detailed standards available without loading every rule into every interaction.

The workflow Skills cover distinct lifecycle activities:

- `project-bootstrap` determines the next useful milestone and stops at the
  earliest decision, clarification, or implementation-approval boundary;
- `technical-decision` compares meaningful options and records an accepted
  ADR-worthy decision without implementing it;
- `implement-approved-batch` implements only the most recently approved batch;
- `verify-change` runs risk-proportionate checks and returns control for user
  review.

See [the Skills guide](../../.agents/README.md) for detailed responsibilities
and invocation guidance.

## Independent Reviewer

The project-scoped reviewer is defined in
[`.codex/agents/reviewer.toml`](../../.codex/agents/reviewer.toml).

It is intended for a separate review pass after implementation and verification
when another perspective would add meaningful confidence. It:

- reconstructs the approved scope;
- checks requirements, accepted ADRs, and engineering standards;
- reviews correctness, architecture, security, regressions, and tests;
- reports prioritized evidence-backed findings; and
- does not implement repairs or authorize Git operations.

The custom agent sets `sandbox_mode = "read-only"`. A parent session's live
runtime overrides can supersede an agent default, so the reviewer instructions
also explicitly prohibit repository modifications.

## Hooks and Command Approval

This repository intentionally has no `.codex/hooks.json`.

The legacy command guard requested interactive approval for selected shell
mutations. Codex `PreToolUse` hooks can allow or deny supported calls, but they
do not support that guard's interactive `ask` result. Mapping `ask` to `deny`
would strengthen the accepted policy; mapping it to `allow` would discard the
safety behavior.

Command approval and sandbox policy therefore remain governed by
[`AGENTS.md`](../../AGENTS.md) and Codex's native sandbox and approval flow.
This limitation and its migration rationale are recorded in
[ADR-0001](decisions/0001-adopt-codex-native-agent-configuration.md) and the
[migration inventory](codex-migration-inventory.md).

Add a future Codex hook only for a concrete recurring requirement whose event,
input, output, failure behavior, trust model, and enforcement semantics are
understood. Do not add a hook merely because a lifecycle event exists.

## Optional Integrations

The repository does not currently define project-level MCP servers, plugins, or
additional custom agents. Add one only when a confirmed project requirement
needs structured external access, distribution, or a genuinely independent
specialist role.

Adding or materially reconfiguring such an integration is a meaningful tooling
or workflow change and must follow the decision and approval boundaries in
`AGENTS.md`.

## Maintenance Checklist

When changing agent configuration:

1. identify the authoritative owner for the behavior;
2. check applicable accepted ADRs before reopening a decision;
3. avoid duplicating normative instructions;
4. preserve Skill and custom-agent triggering descriptions;
5. verify version-sensitive Codex behavior against current official
   documentation;
6. keep optional profiles conditional unless the project explicitly adopts
   them;
7. run targeted format, parse, link, and parity checks; and
8. obtain separate approval for implementation, removal, and Git operations as
   required.

## Official References

- [Custom instructions with `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Build Skills](https://learn.chatgpt.com/docs/build-skills)
- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Hooks](https://learn.chatgpt.com/docs/hooks)
