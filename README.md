# Codex Python Boilerplate

Codex Python Boilerplate is an opinionated, Codex-native foundation for new
Python projects. It combines a human-controlled agent workflow with
progressively loaded engineering standards, a project-scoped reviewer, and a
reproducible Python quality toolchain.

The repository intentionally contains no product behavior. Its package and
single smoke test exist only to keep packaging, linting, type checking, import
rules, testing, and coverage executable from the first commit.

## Included

- a concise root `AGENTS.md` working agreement;
- repository Skills under `.agents/skills/`;
- an independent reviewer under `.codex/agents/`;
- project-definition and ADR templates;
- Python 3.14 managed with `uv`;
- Ruff, Pyright, pytest, coverage, Import Linter, and pre-commit;
- shared VS Code recommendations and settings.

## Start a Project

Create or synchronize the environment:

```bash
uv sync
```

Install the Git hooks:

```bash
uv run pre-commit install --hook-type pre-commit
uv run pre-commit install --hook-type pre-push
```

Run the complete local verification:

```bash
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
uv build
```

Before implementing product behavior, follow the
[customization checklist](docs/project/customization.md), complete the
[project definition](docs/project/definition.md), and ask Codex to start the
project.

## Agent Configuration

The [agent-configuration guide](docs/project/agent-configuration.md) explains
how `AGENTS.md`, repository Skills, project decisions, and the independent
reviewer fit together.

## Distribution

This boilerplate is distributed under the [MIT License](LICENSE). Derived
projects must preserve the license notice for copied boilerplate content.

The boilerplate deliberately does not select a hosting provider or CI platform.
Choose those integrations while customizing the derived project.
