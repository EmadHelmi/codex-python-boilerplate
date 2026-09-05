# Codex Python Boilerplate

An opinionated Codex-native foundation for Python projects with a
human-controlled development workflow, progressively loaded engineering
standards, reproducible quality tooling, and selectable source-control hosting.

[![CI](https://github.com/EmadHelmi/codex-python-boilerplate/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/EmadHelmi/codex-python-boilerplate/actions/workflows/ci.yml)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Use this template](https://img.shields.io/badge/Use_this_template-2EA44F?style=for-the-badge&logo=github&logoColor=white)](https://github.com/EmadHelmi/codex-python-boilerplate/generate)
[![Contribute](https://img.shields.io/badge/Contribute-0969DA?style=for-the-badge&logo=github&logoColor=white)](CONTRIBUTING.md)

## Start an Independent Project

Create an independent repository rather than a fork unless you intend to
contribute changes back to this boilerplate. Then follow the single linear
[Getting Started guide](docs/getting-started.md) from repository creation
through project setup and verification.

The [customization reference](docs/project/customization.md) explains the
available setup fields and generated behavior. Consult it when choosing values;
the executable sequence remains in Getting Started.

## What the Baseline Provides

- Python 3.14 dependency and environment management with uv;
- Ruff, Pyright, pytest, coverage, Import Linter, and pre-commit;
- a root `AGENTS.md` working agreement;
- repository Skills and progressively loaded engineering standards;
- a project-scoped independent Codex reviewer;
- project-definition and Architecture Decision Record foundations;
- GitHub and GitLab automation plus provider-neutral output;
- deterministic, preview-first project customization.

The boilerplate intentionally does not select application architecture,
framework dependencies, infrastructure, deployment, or product requirements.

## Develop the Boilerplate

Create the environment and install hooks:

```bash
uv sync --locked
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Run the complete local quality gate:

```bash
uv lock --check
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
uv build
```

Read [Contributing](CONTRIBUTING.md) before proposing changes. Usage questions
belong in [Support](SUPPORT.md), and vulnerabilities must follow the private
process in [Security](SECURITY.md).

## Documentation

- [Getting Started](docs/getting-started.md)
- [Customizing the Boilerplate](docs/project/customization.md)
- [Development Tooling](docs/development-tooling.md)
- [Agent Configuration](docs/project/agent-configuration.md)
- [Project Definition](docs/project/definition.md)
- [Architecture Decisions](docs/project/decisions/README.md)

## License

The boilerplate is distributed under the [MIT License](LICENSE). Projects that
choose another license must preserve the boilerplate notice as described in
the customization guide.
