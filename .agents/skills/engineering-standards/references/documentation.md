<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Documentation Standards

Classification: **HYBRID**.

Application: Read when creating or changing Markdown or repository documentation.

## Mechanical Markdown Rules

- Before creating or editing Markdown, inspect `pyproject.toml` for `[tool.markdownlint-cli2.config]` when it exists.
  Treat configured markdownlint rules as authoritative for mechanical Markdown style.
- Do not duplicate, reinterpret, or override lintable formatting rules in prose. If Markdown tooling is configured
  elsewhere, follow that configuration instead.
- When no Markdown linter configuration exists, preserve established repository style instead of introducing a new
  convention during unrelated work.

## Navigation

- Add a table of contents only when document length or heading depth makes navigation materially easier.
- Consider one when a document exceeds roughly one page of normal reading, has many major sections, or contains
  multiple heading levels.
- Prefer a collapsible HTML `details`/`summary` table of contents only when the renderer and Markdown configuration
  support it. Otherwise use the clearest supported form.
- Keep a table of contents synchronized whenever headings change.
- Do not add one to a short document when it creates more noise than value.

## Documentation Quality

- Write for the reader's task. Establish purpose, scope, prerequisites, or the important decision before detailed
  implementation when that context is necessary.
- Keep documentation concise and scannable without removing information needed to understand, operate, maintain, or
  safely change the documented behavior.
- Prefer one authoritative source for facts that can drift, including configuration, supported versions, defaults,
  generated values, and commands. Reference the owner instead of duplicating facts unless duplication materially
  improves usability and has a clear maintenance owner.
- Use repository-relative links for local files when practical, with descriptive link text.
- Keep commands and examples copyable and faithful to their stated environment. Omit shell prompt characters unless
  intentionally showing a transcript.
- Distinguish normative requirements from examples, suggestions, historical notes, and illustrative values whenever
  confusion could affect system use.
- Use prose for explanation, lists for steps or compact collections, tables for structured comparisons, and diagrams
  for relationships or flows. Prefer the simplest representation that communicates clearly.
- Preserve established project terminology, public names, identifiers, commands, and configuration keys exactly.
- Support progressive reading with headings, summaries, tables, diagrams, and collapsible sections when they improve
  comprehension.

## Diagrams

- When a conceptual graph, architecture, workflow, state transition, sequence, or dependency would otherwise be ASCII
  art or a plain-text diagram, use Mermaid when the renderer supports it and Mermaid expresses the concept clearly.
- Select the diagram type that matches the semantics, such as `flowchart`, `sequenceDiagram`, `classDiagram`,
  `stateDiagram-v2`, `erDiagram`, `gitGraph`, or `mindmap`.
- Keep diagrams simple and portable. Prefer meaningful labels and explicit boundaries over decoration, custom themes,
  renderer-specific tricks, or complex layout hacks.
- Use valid Mermaid syntax. If the supported version cannot express the model reliably, use the clearest supported
  representation and explain the relationship in prose when needed.
- Keep exact text artifacts literal: filesystem trees, command output, logs, stack traces, protocol transcripts,
  configuration examples, and source code are not conceptual diagrams.
- Do not add a diagram when a sentence, list, or table is clearer.
- Give important diagrams enough surrounding prose that their critical meaning remains accessible without rendering.

## Tables

- Center-align columns with `:---:` by default when explicit alignment improves consistency and readability.
- Override alignment per column when another choice is easier to read: `:---` for left, `---:` for right, or `---` when
  forced alignment adds no value.
- Preserve intentional alignment in existing tables unless a change clearly improves readability.
