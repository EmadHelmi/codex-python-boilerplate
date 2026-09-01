# ADR-0001: Use Codex-Native Repository Configuration

- Status: `Accepted`
- Date: 2026-09-01

## Context

The boilerplate needs a repository-owned configuration that Codex can discover
without relying on another coding agent's proprietary rule, agent, or hook
formats. It must preserve detailed engineering standards without loading all
guidance into every task, keep important human approval boundaries explicit,
and provide an optional independent review path.

## Decision Drivers

- Use documented Codex-native repository mechanisms.
- Keep instruction loading efficient and maintainable.
- Preserve explicit human control over decisions, implementation, and Git.
- Keep one canonical owner for each requirement or rule.
- Make the foundation reusable across Python projects.
- Avoid integrations whose permissions or semantics depend on an unconfirmed
  derived-project requirement.

## Decision

The boilerplate uses:

1. a concise root `AGENTS.md` as the authoritative human-agent working
   agreement;
2. repository Skills under `.agents/skills/` for focused workflows and
   progressively loaded engineering standards;
3. mandatory routing from `AGENTS.md` to applicable repository Skills;
4. `docs/project/definition.md` for product requirements in derived projects;
5. accepted ADRs under `docs/project/decisions/` for meaningful active
   technical decisions;
6. a narrow, report-only reviewer under `.codex/agents/`.

The boilerplate does not maintain parallel configuration for other coding
agents. It also does not include Codex hooks, MCP servers, plugins, or
provider-specific CI by default. A derived project may add one only for a
confirmed requirement after evaluating permissions, trust boundaries, runtime
semantics, failure behavior, and maintenance cost.

All repository documentation, code, comments, identifiers, and configuration
are written in English unless the user explicitly requests another language
for a specific part.

## Consequences

### Positive

- Codex can discover repository guidance through native mechanisms.
- Progressive disclosure keeps the root instruction budget small.
- Workflow, product definition, decisions, and engineering rules have distinct
  authoritative owners.
- The reviewer adds independent evidence without gaining repair authority.
- Derived projects begin without unnecessary external integrations.

### Negative

- Other coding agents do not receive tool-specific repository configuration.
- Correct behavior depends on precise Skill descriptions and routing.
- Derived projects must deliberately add any required integration or CI
  configuration.

## Alternatives Considered

### Put All Guidance in `AGENTS.md`

This would make every rule immediately visible, but it would consume the
project-instruction budget, load irrelevant detail, and create duplication.

### Maintain Multiple Agent-specific Configurations

This could provide first-class behavior in several tools, but it would create
parallel sources that can drift in meaning and enforcement.

### Use Only `AGENTS.md` Without Skills or a Reviewer

This would be simpler structurally, but it would remove progressive disclosure
and the optional independent review path required by the boilerplate.

## References

- [`AGENTS.md`](../../../AGENTS.md)
- [Repository agent configuration](../agent-configuration.md)
- [Codex custom instructions with `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex Skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
