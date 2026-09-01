# Agent Skills

This directory contains repository-scoped Skills for the human-controlled
development workflow and progressively loaded engineering standards.

Skills explain how to perform focused work. They do not define the product,
grant mutation approval, or replace the root working agreement.

## Structure

```text
.agents/
├── README.md
└── skills/
    ├── engineering-standards/
    │   ├── SKILL.md
    │   └── references/
    ├── implement-approved-batch/
    │   └── SKILL.md
    ├── project-bootstrap/
    │   └── SKILL.md
    ├── technical-decision/
    │   └── SKILL.md
    └── verify-change/
        └── SKILL.md
```

Codex discovers these Skills from `.agents/skills/`. It can select a Skill
implicitly when the task matches its frontmatter description, or the user can
invoke one explicitly by name.

## Responsibilities

| Skill | Use it when |
| :--- | :--- |
| `engineering-standards` | Planning, implementing, reviewing, or verifying code, tests, documentation, architecture, tooling, or Git workflow changes |
| `project-bootstrap` | Starting or resuming a project and determining the next useful milestone |
| `technical-decision` | A meaningful unresolved technical or architectural choice blocks current work |
| `implement-approved-batch` | The user has explicitly approved a sufficiently clear implementation scope |
| `verify-change` | Approved implementation is complete and needs risk-proportionate verification |

The authoritative workflow remains [`AGENTS.md`](../AGENTS.md):

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

Each workflow Skill owns only its portion of that lifecycle and returns control
at the next human boundary.

## Engineering Standards

`engineering-standards/SKILL.md` is a router. It loads
`references/governance.md` and only the additional references that apply to
the current concern. This progressive-disclosure design keeps detailed rules
available without adding unrelated guidance to every task.

Optional profiles such as strict branch discipline and per-file authorship
remain inactive until a derived project explicitly adopts them.

## Maintaining Skills

When adding or changing a Skill:

1. keep one focused job per Skill;
2. make the frontmatter description precise enough for implicit selection;
3. keep mandatory shared behavior in `SKILL.md`;
4. route substantial conditional detail to focused references;
5. do not duplicate `AGENTS.md`, project requirements, or ADRs;
6. preserve approval and Git boundaries;
7. validate frontmatter, links, Markdown, and realistic behavior.

See the [agent-configuration guide](../docs/project/agent-configuration.md) for
the complete repository model.
