# Development Tooling

Executable configuration remains authoritative over this overview.

| Tool | Responsibility | Configuration |
| :--- | :--- | :--- |
| uv | Python environment, dependencies, and lockfile | `pyproject.toml`, `uv.lock`, `.python-version` |
| Ruff | Formatting, linting, and import ordering | `pyproject.toml` |
| Pyright | Reproducible static type checking | `pyproject.toml` |
| pytest and coverage.py | Behavioral tests and coverage threshold | `pyproject.toml` |
| Import Linter | Executable package-boundary contracts | `pyproject.toml` |
| pre-commit | Local pre-commit and pre-push orchestration | `.pre-commit-config.yaml` |
| GitHub Actions or GitLab CI | Hosted execution for the selected profile | `.github/workflows/` or `.gitlab-ci.yml` |

## Local Quality Gate

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest --cov --cov-report=term-missing
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
```

Use `uv add`, `uv add --dev`, and `uv remove` for dependency changes. Do not
edit `uv.lock` manually. Run project tools through `uv run`.

## Hosted Automation

The GitHub profile runs the local gate in GitHub Actions, validates pull-request
metadata for collaborative projects, reviews dependency changes, and configures
scheduled dependency updates. The GitLab profile runs the local gate in GitLab
CI and validates merge-request metadata for collaborative projects. GitLab
security and dependency-update capabilities vary by deployment and must be
enabled deliberately according to `.gitlab/REPOSITORY_SETTINGS.md`.

The `uv-pre-commit` revision is intentionally excluded from automated
pre-commit updates. Upgrade it manually in the same change as `UV_VERSION` in
`.github/workflows/ci.yml`; the publication tests require those two versions
to remain identical.

The neutral profile contains no hosted automation. This is intentional and
does not weaken the local quality gate.
