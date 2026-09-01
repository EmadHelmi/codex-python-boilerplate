# Boilerplate Customization

Complete this checklist after copying the boilerplate and before implementing
product behavior.

## 1. Rename the Project

Choose three related identifiers:

| Identifier | Example | Used for |
| :--- | :--- | :--- |
| Distribution name | `example-service` | `project.name`, package builds, and the virtual-environment prompt |
| Import package | `example_service` | `src/`, imports, coverage, and Import Linter |
| Display name | `Example Service` | README and human-facing documentation |

Replace the boilerplate identifiers in:

- `pyproject.toml`;
- `.pre-commit-config.yaml`;
- `src/codex_boilerplate/`;
- `tests/test_package.py`;
- `README.md`;
- `uv.lock`, by running `uv lock` rather than editing it manually.

Search the tracked repository afterward:

```bash
rg -n --hidden --glob '!.git/**' \
  'codex-python-boilerplate|codex_boilerplate|Codex Python Boilerplate'
```

## 2. Recreate the Local Environment

The activation prompt is local environment metadata and is not committed.
Recreate the environment after changing `project.name`:

```bash
uv venv --clear --prompt example-service
uv sync
```

Replace `example-service` with the selected distribution name.

## 3. Define the Product

Complete `docs/project/definition.md`. Remove instructional placeholders,
resolve only decisions required for the first useful milestone, and record
accepted ADR-worthy decisions under `docs/project/decisions/`.

Do not retain boilerplate examples as product requirements.

## 4. Review the Engineering Baseline

Confirm or deliberately change:

- the Python version in `.python-version` and `pyproject.toml`;
- package metadata and runtime dependencies;
- Ruff, Pyright, pytest, coverage, and Import Linter settings;
- optional engineering profiles in
  `.agents/skills/engineering-standards/references/`;
- VS Code recommendations;
- pre-commit and pre-push hooks.

Update version-sensitive reviewed baselines only after reviewing the
corresponding standards against the selected tool versions.

## 5. Review Legal Terms and Project-owned Integrations

The boilerplate is licensed under MIT. Preserve its copyright and permission
notice for copied boilerplate content. Add project-specific copyright notices
or compatible licensing only when the derived project's ownership and
distribution requirements are understood.

Add only integrations required by the derived project:

- the appropriate Git remote and hosting metadata;
- CI/CD for the selected provider;
- issue, release, security, and contribution policies;
- MCP servers, plugins, Codex hooks, or additional custom agents.

These choices are intentionally not inherited from the boilerplate because
their correct values depend on the derived project.

## 6. Verify the Customized Foundation

```bash
uv lock --check
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
uv build
```

Inspect `git diff` and confirm that no boilerplate identity remains where the
new project identity should appear.
