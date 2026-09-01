# Repository Agent Configuration

This guide explains the boilerplate's Codex-native configuration and the
responsibility of each source.

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
├── customization.md
├── definition.md
└── decisions/
```

## Sources of Truth

| Source | Responsibility |
| :--- | :--- |
| [`AGENTS.md`](../../AGENTS.md) | Human-agent workflow, approval boundaries, scope control, review, and Git authorization |
| [Engineering standards](../../.agents/skills/engineering-standards/SKILL.md) | Routing to applicable coding, testing, architecture, tooling, documentation, and repository standards |
| [Workflow Skills](../../.agents/README.md) | Focused procedures for bootstrap, decisions, approved implementation, and verification |
| [Project definition](definition.md) | Product goals, scope, requirements, constraints, and definition of done |
| [Accepted ADRs](decisions/README.md) | Active meaningful technical and architectural decisions |
| [Reviewer](../../.codex/agents/reviewer.toml) | Optional independent, report-only review after verification |

Keep one authoritative owner for each normative statement. Link to the owner
instead of copying its rules elsewhere.

## Working Agreement

Codex reads the root `AGENTS.md` before work. The file defines the
human-controlled lifecycle:

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

It also routes applicable work to repository Skills. The concise root file is
kept safely below Codex's default combined project-instruction size limit so
that user-level instructions and future scoped files have room.

## Skills

Codex discovers repository Skills under `.agents/skills/`. It initially sees
each Skill's name and description, then loads the full `SKILL.md` only when
the task matches or the user invokes it explicitly.

The `engineering-standards` Skill provides progressive disclosure: it loads
governance first and then only the references relevant to the current concern.
The workflow Skills cover distinct lifecycle activities:

- `project-bootstrap` establishes the next useful milestone and stops at the
  earliest decision, context, or approval boundary;
- `technical-decision` evaluates a required meaningful choice and records an
  accepted ADR-worthy decision without implementing it;
- `implement-approved-batch` executes only explicitly approved scope;
- `verify-change` performs proportionate checks and returns control for user
  review.

See the [Skills guide](../../.agents/README.md) for invocation and maintenance
guidance.

## Independent Reviewer

The project-scoped `reviewer` is a narrow custom agent under
`.codex/agents/reviewer.toml`. Use it after implementation and verification
when an independent perspective is likely to improve confidence. It
reconstructs approved scope, evaluates the result against authoritative
context, and reports prioritized evidence-backed findings without modifying
the repository.

The reviewer inherits the parent session's live permission policy. Its
`sandbox_mode = "read-only"` default and explicit report-only instructions
provide defense in depth, but do not replace the parent's approval controls.

## Hooks, MCP, and Plugins

The boilerplate does not define repository hooks, MCP servers, or plugins.
These integrations are valuable only when a derived project has a concrete
recurring requirement and understands the integration's permissions, trust
boundary, failure behavior, and maintenance cost.

Pre-commit is repository quality automation, not a Codex lifecycle hook.
Command approval remains governed by `AGENTS.md` and Codex's native sandbox
and approval flow.

## Maintenance Checklist

When changing agent configuration:

1. identify the authoritative owner for the behavior;
2. check applicable accepted ADRs;
3. use the narrowest native mechanism;
4. avoid duplicated normative instructions;
5. keep Skill descriptions concise and discriminating;
6. verify version-sensitive behavior against official documentation;
7. run format, parse, link, and behavioral checks; and
8. preserve implementation, review, and Git approval boundaries.

## Official References

- [Custom instructions with `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Build Skills](https://learn.chatgpt.com/docs/build-skills)
- [Subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Hooks](https://learn.chatgpt.com/docs/hooks)
