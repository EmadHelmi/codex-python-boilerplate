"""Turn a fresh Codex Python Boilerplate repository into a real project."""

from __future__ import annotations

import argparse
import keyword
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal
from urllib.parse import urlsplit

Host = Literal["github", "gitlab", "neutral"]
Collaboration = Literal["solo", "collaborative"]
LicenseChoice = Literal["mit", "unset"]

BOILERPLATE_DISTRIBUTION: Final = "codex-python-boilerplate"
BOILERPLATE_PACKAGE: Final = "codex_boilerplate"
BOILERPLATE_DISPLAY_NAME: Final = "Codex Python Boilerplate"
BOILERPLATE_DESCRIPTION: Final = (
    "An opinionated Codex-native foundation for Python projects"
)
BOILERPLATE_AUTHORS: Final = (
    'authors = [{ name = "Emad Helmi", email = "s.emad.helmi@gmail.com" }]'
)
BOILERPLATE_REPOSITORY_URL: Final = (
    "https://github.com/EmadHelmi/codex-python-boilerplate"
)
NEUTRAL_TEMPLATE_WORKFLOW: Final = (
    "your source-control platform's template or repository-copy workflow"
)
GITLAB_TEMPLATE_ROOT: Final = Path("templates/providers/gitlab")
COMMUNITY_FILES: Final = (
    Path("CODE_OF_CONDUCT.md"),
    Path("CONTRIBUTING.md"),
    Path("GOVERNANCE.md"),
    Path("SECURITY.md"),
    Path("SUPPORT.md"),
)
GITHUB_COLLABORATION_PATHS: Final = (
    Path(".github/CODEOWNERS"),
    Path(".github/ISSUE_TEMPLATE"),
    Path(".github/pull_request_template.md"),
    Path(".github/rulesets"),
    Path(".github/scripts/validate_pr.py"),
    Path(".github/workflows/pr-policy.yml"),
)
GITLAB_COLLABORATION_PATHS: Final = (
    Path(".gitlab/CODEOWNERS"),
    Path(".gitlab/issue_templates"),
    Path(".gitlab/merge_request_templates"),
    Path(".gitlab/scripts/validate_mr.py"),
)
TEMPLATE_ONLY_PATHS: Final = (
    Path("templates"),
    Path("scripts/setup_project.py"),
    Path("tests/test_project_setup.py"),
    Path("tests/test_repository_publication.py"),
    Path("docs/README.md"),
    Path("docs/development-tooling.md"),
    Path("docs/getting-started.md"),
    Path("docs/project/customization.md"),
)
BOILERPLATE_ADRS: Final = (
    Path(
        "docs/project/decisions/"
        "0001-use-codex-native-repository-configuration.md"
    ),
    Path("docs/project/decisions/0002-license-the-boilerplate-under-mit.md"),
    Path(
        "docs/project/decisions/"
        "0003-separate-host-and-collaboration-profiles.md"
    ),
)
GITLAB_COLLABORATIVE_START: Final = "# setup:collaborative:start"
GITLAB_COLLABORATIVE_END: Final = "# setup:collaborative:end"
DISTRIBUTION_PATTERN: Final = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
PACKAGE_PATTERN: Final = re.compile(r"^[a-z][a-z0-9_]*$")
CODE_OWNER_PATTERN: Final = re.compile(
    r"^@[A-Za-z0-9][A-Za-z0-9_.-]*"
    r"(?:/[A-Za-z0-9][A-Za-z0-9_.-]*)*$"
)
PUBLISH_PATHS: Final = (
    Path(".github"),
    Path(".gitlab"),
    Path(".gitlab-ci.yml"),
    Path(".pre-commit-config.yaml"),
    *COMMUNITY_FILES,
    Path("LICENSE"),
    Path("THIRD_PARTY_NOTICES.md"),
    Path("README.md"),
    Path("pyproject.toml"),
    Path("uv.lock"),
    Path("src"),
    Path("tests"),
    Path("templates"),
    Path("scripts"),
    Path("docs"),
)


class ProjectSetupError(RuntimeError):
    """Report an unsafe or inconsistent project-setup operation."""


@dataclass(frozen=True)
class SetupConfig:
    """Describe one deterministic project setup."""

    host: Host
    collaboration: Collaboration
    distribution_name: str
    import_package: str
    display_name: str
    description: str
    author_name: str
    author_email: str
    project_license: LicenseChoice
    repository_url: str | None
    code_owner: str | None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise ProjectSetupError(f"Cannot read {path}.") from error


def _write_text(path: Path, content: str) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        raise ProjectSetupError(f"Cannot write {path}.") from error


def _remove_path(path: Path) -> None:
    try:
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    except OSError as error:
        raise ProjectSetupError(f"Cannot remove {path}.") from error


def _replace_once(content: str, old: str, new: str, *, label: str) -> str:
    if content.count(old) != 1:
        raise ProjectSetupError(
            f"Expected exactly one {label}; found {content.count(old)}."
        )
    return content.replace(old, new, 1)


def validate_config(config: SetupConfig) -> None:
    """Reject incomplete or unsafe setup values."""

    if DISTRIBUTION_PATTERN.fullmatch(config.distribution_name) is None:
        raise ProjectSetupError("Distribution name is not valid.")
    if PACKAGE_PATTERN.fullmatch(config.import_package) is None:
        raise ProjectSetupError("Import package must be a Python identifier.")
    for label, value in (
        ("display name", config.display_name),
        ("description", config.description),
        ("author name", config.author_name),
        ("author email", config.author_email),
    ):
        if not value.strip() or "\n" in value or '"' in value or "\\" in value:
            raise ProjectSetupError(f"The {label} must be one non-empty line.")
    if "@" not in config.author_email:
        raise ProjectSetupError("Author email is not valid.")
    if keyword.iskeyword(config.import_package):
        raise ProjectSetupError("Import package must not be a Python keyword.")
    if config.host == "neutral":
        if config.repository_url is not None or config.code_owner is not None:
            raise ProjectSetupError(
                "Neutral projects cannot use provider-specific repository "
                "or Code Owner values."
            )
    elif (
        config.collaboration == "collaborative"
        and config.repository_url is None
    ):
        raise ProjectSetupError(
            "Collaborative GitHub and GitLab projects require "
            "--repository-url."
        )
    elif config.repository_url is not None:
        _validate_repository_url(config.host, config.repository_url)
    if (
        config.collaboration == "collaborative"
        and config.host != "neutral"
        and config.code_owner is None
    ):
        raise ProjectSetupError(
            "Collaborative hosted projects require --code-owner."
        )
    if (
        config.code_owner is not None
        and CODE_OWNER_PATTERN.fullmatch(config.code_owner) is None
    ):
        raise ProjectSetupError(
            "Code Owner must be one @user, @group, or @group/subgroup value."
        )


def _validate_repository_url(host: Host, repository_url: str) -> None:
    """Require a safe HTTPS project URL compatible with the selected host."""

    if any(character.isspace() for character in repository_url) or any(
        character in repository_url for character in ('"', "'", "\\")
    ):
        raise ProjectSetupError("Repository URL must be one safe HTTPS URL.")
    parsed = urlsplit(repository_url)
    if (
        parsed.scheme != "https"
        or parsed.hostname is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path in ("", "/")
    ):
        raise ProjectSetupError("Repository URL must be one safe HTTPS URL.")
    hostname = parsed.hostname.casefold()
    if host == "github" and "gitlab" in hostname:
        raise ProjectSetupError("Repository URL conflicts with GitHub host.")
    if host == "gitlab" and "github" in hostname:
        raise ProjectSetupError("Repository URL conflicts with GitLab host.")


def validate_root(root: Path) -> Path:
    """Return a fresh boilerplate root or reject another directory."""

    resolved = root.resolve()
    required = (
        Path("AGENTS.md"),
        Path(".agents"),
        Path(".codex/agents/reviewer.toml"),
        Path(".github/workflows/ci.yml"),
        GITLAB_TEMPLATE_ROOT / ".gitlab-ci.yml",
        Path("pyproject.toml"),
        Path(f"src/{BOILERPLATE_PACKAGE}/__init__.py"),
        Path("tests/test_package.py"),
    )
    missing = [path for path in required if not (resolved / path).exists()]
    if missing:
        paths = ", ".join(path.as_posix() for path in missing)
        raise ProjectSetupError(
            f"Not a fresh boilerplate root; missing: {paths}."
        )

    pyproject = _read_text(resolved / "pyproject.toml")
    if f'name = "{BOILERPLATE_DISTRIBUTION}"' not in pyproject:
        raise ProjectSetupError("The project has already been customized.")
    return resolved


def planned_actions(root: Path, config: SetupConfig) -> tuple[str, ...]:
    """Validate setup and return a stable human-readable mutation plan."""

    validate_config(config)
    validate_root(root)
    actions = [
        f"select {config.host}/{config.collaboration} profile",
        f"rename distribution to {config.distribution_name}",
        f"rename import package to {config.import_package}",
        "rewrite project metadata, README, and package smoke test",
        "reset project definition and ADRs for the derived project",
        "remove one-time boilerplate setup files",
    ]
    if config.project_license == "unset":
        actions.append("preserve MIT provenance without licensing the project")
    actions.append("regenerate uv.lock")
    return tuple(actions)


def _project_urls(config: SetupConfig) -> str:
    if config.repository_url is None:
        raise ProjectSetupError("Cannot render project URLs without a URL.")
    url = config.repository_url.rstrip("/")
    route = "/-" if config.host == "gitlab" else ""
    return (
        "[project.urls]\n"
        f'Documentation = "{url}{route}/tree/main/docs"\n'
        f'Issues = "{url}{route}/issues"\n'
        f'Repository = "{url}"\n\n'
    )


def _coverage_source(config: SetupConfig) -> str:
    sources = [f'"src/{config.import_package}"']
    if config.collaboration == "collaborative":
        if config.host == "github":
            sources.append('".github/scripts"')
        elif config.host == "gitlab":
            sources.append('".gitlab/scripts"')
    return f"source = [{', '.join(sources)}]"


def _authors(config: SetupConfig) -> str:
    return (
        f'authors = [{{ name = "{config.author_name}", '
        f'email = "{config.author_email}" }}]'
    )


def _remove_toml_table(content: str, header: str) -> str:
    lines = content.splitlines(keepends=True)
    indexes = [
        index for index, line in enumerate(lines) if line.strip() == header
    ]
    if not indexes:
        return content
    if len(indexes) != 1:
        raise ProjectSetupError(f"TOML table {header} is ambiguous.")
    start = indexes[0]
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].lstrip().startswith("[")
        ),
        len(lines),
    )
    del lines[start:end]
    return "".join(lines)


def _customize_pyproject(root: Path, config: SetupConfig) -> None:
    path = root / "pyproject.toml"
    content = _read_text(path)
    replacements = (
        (
            f'name = "{BOILERPLATE_DISTRIBUTION}"',
            f'name = "{config.distribution_name}"',
            "distribution name",
        ),
        (
            f'description = "{BOILERPLATE_DESCRIPTION}"',
            f'description = "{config.description}"',
            "project description",
        ),
        (
            BOILERPLATE_AUTHORS,
            _authors(config),
            "project authors",
        ),
        (
            f'module-name = "{BOILERPLATE_PACKAGE}"',
            f'module-name = "{config.import_package}"',
            "build module name",
        ),
        (
            (
                f'source = ["src/{BOILERPLATE_PACKAGE}", '
                '".github/scripts", "scripts", '
                '"templates/providers/gitlab/.gitlab/scripts"]'
            ),
            _coverage_source(config),
            "coverage source",
        ),
        (
            f'root_package = "{BOILERPLATE_PACKAGE}"',
            f'root_package = "{config.import_package}"',
            "Import Linter root",
        ),
        (
            f'ancestors = ["{BOILERPLATE_PACKAGE}"]',
            f'ancestors = ["{config.import_package}"]',
            "Import Linter ancestors",
        ),
    )
    for old, new, label in replacements:
        content = _replace_once(content, old, new, label=label)

    content = _remove_toml_table(content, "[project.urls]")
    if config.repository_url is not None:
        marker = "dependencies = []\n\n"
        content = _replace_once(
            content,
            marker,
            f"{marker}{_project_urls(config)}",
            label="project URL insertion point",
        )

    if config.project_license == "unset":
        content = _replace_once(
            content, 'license = "MIT"\n', "", label="MIT license field"
        )
        content = _replace_once(
            content,
            'license-files = ["LICENSE"]\n',
            'license-files = ["THIRD_PARTY_NOTICES.md"]\n',
            label="license files field",
        )
    _write_text(path, content)


def _customize_package(root: Path, config: SetupConfig) -> None:
    old_package = root / "src" / BOILERPLATE_PACKAGE
    new_package = root / "src" / config.import_package
    if new_package.exists():
        raise ProjectSetupError(
            f"Target package already exists: {new_package}."
        )
    try:
        old_package.replace(new_package)
    except OSError as error:
        raise ProjectSetupError("Cannot rename the import package.") from error
    _write_text(
        new_package / "__init__.py",
        f'"""{config.display_name} package."""\n',
    )

    test_path = root / "tests/test_package.py"
    test = _read_text(test_path).replace(
        BOILERPLATE_PACKAGE, config.import_package
    )
    _write_text(test_path, test)

    hooks_path = root / ".pre-commit-config.yaml"
    hooks = _read_text(hooks_path).replace(
        f"src/{BOILERPLATE_PACKAGE}", f"src/{config.import_package}"
    )
    _write_text(hooks_path, hooks)


def _render_readme(config: SetupConfig) -> str:
    repository = (
        f"\nRepository: [{config.repository_url}]({config.repository_url})\n"
        if config.repository_url is not None
        else ""
    )
    return f"""# {config.display_name}

{config.description}
{repository}
## Development

Create the environment and install the local quality hooks:

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

Define product scope in `docs/project/definition.md` before implementing the
first product milestone. Record only accepted, project-specific decisions in
`docs/project/decisions/`.
"""


def _render_solo_settings(config: SetupConfig) -> str:
    platform = "GitHub" if config.host == "github" else "GitLab"
    checks = (
        "`Quality gate`, `Compatibility gate`, and "
        "`Review dependency changes`."
        if config.host == "github"
        else "the `quality` pipeline job."
    )
    return f"""# {platform} Repository Settings for a Solo Project

Use this file as a remote-settings checklist after publishing the project.

- Set `main` as the default branch.
- Protect `main` from deletion and force-pushes.
- Keep CI enabled. When the hosting plan supports required checks, require
  {checks}
- Prefer squash merging and delete merged branches automatically.
- Store secrets in the hosting platform, never in the repository.

This solo profile intentionally has no mandatory reviewer, approval count,
Code Owner, issue template, or change-proposal metadata policy. Tighten these
settings later if the project gains collaborators.
"""


def _materialize_host(root: Path, config: SetupConfig) -> None:
    if config.host == "github":
        _remove_path(root / ".gitlab")
        _remove_path(root / ".gitlab-ci.yml")
        if config.collaboration == "solo":
            for path in GITHUB_COLLABORATION_PATHS:
                _remove_path(root / path)
            _write_text(
                root / ".github/REPOSITORY_SETTINGS.md",
                _render_solo_settings(config),
            )
        elif config.code_owner is not None:
            codeowners = root / ".github/CODEOWNERS"
            _write_text(
                codeowners,
                _read_text(codeowners).replace(
                    "@EmadHelmi", config.code_owner
                ),
            )
    elif config.host == "gitlab":
        _remove_path(root / ".github")
        template = root / GITLAB_TEMPLATE_ROOT
        try:
            shutil.copy2(template / ".gitlab-ci.yml", root / ".gitlab-ci.yml")
            shutil.copytree(template / ".gitlab", root / ".gitlab")
        except OSError as error:
            raise ProjectSetupError(
                "Cannot materialize GitLab files."
            ) from error
        if config.collaboration == "solo":
            for path in GITLAB_COLLABORATION_PATHS:
                _remove_path(root / path)
            _write_text(
                root / ".gitlab/REPOSITORY_SETTINGS.md",
                _render_solo_settings(config),
            )
            ci_path = root / ".gitlab-ci.yml"
            _write_text(
                ci_path,
                _without_marked_section(
                    _read_text(ci_path),
                    GITLAB_COLLABORATIVE_START,
                    GITLAB_COLLABORATIVE_END,
                ),
            )
        elif config.code_owner is not None:
            codeowners = root / ".gitlab/CODEOWNERS"
            _write_text(
                codeowners,
                _read_text(codeowners).replace(
                    "@EmadHelmi", config.code_owner
                ),
            )
    else:
        _remove_path(root / ".github")
        _remove_path(root / ".gitlab")
        _remove_path(root / ".gitlab-ci.yml")


def _without_marked_section(content: str, start: str, end: str) -> str:
    if content.count(start) != 1 or content.count(end) != 1:
        raise ProjectSetupError("A profile marker is missing or ambiguous.")
    before, remainder = content.split(start, 1)
    _, after = remainder.split(end, 1)
    return f"{before.rstrip()}\n{after.lstrip()}"


def _adapt_collaborative_docs(root: Path, config: SetupConfig) -> None:
    if config.collaboration == "solo":
        for path in COMMUNITY_FILES:
            _remove_path(root / path)
        return

    replacements: tuple[tuple[str, str], ...]
    if config.host == "gitlab":
        replacements = (
            (
                "GitHub's **Use this template** action",
                "the approved GitLab project template workflow",
            ),
            ("pull requests", "merge requests"),
            ("pull request", "merge request"),
            ("Pull Requests", "Merge Requests"),
            ("GitHub grants", "GitLab grants"),
            ("GitHub", "GitLab"),
            ("Dependabot", "automated dependency-update"),
        )
    elif config.host == "neutral":
        replacements = (
            (
                "GitHub's **Use this template** action",
                NEUTRAL_TEMPLATE_WORKFLOW,
            ),
            ("pull requests", "change proposals"),
            ("pull request", "change proposal"),
            ("Pull Requests", "Change Proposals"),
            ("GitHub grants", "hosting platform grants"),
            ("GitHub", "the hosting platform"),
            ("Dependabot", "automated dependency-update"),
        )
    else:
        replacements = ()

    for relative_path in COMMUNITY_FILES:
        path = root / relative_path
        if relative_path == Path("SECURITY.md") and config.host != "github":
            _write_text(path, _render_private_security_policy(config))
            continue
        content = _read_text(path)
        content = content.replace(
            "AI-Native Python Project Boilerplate", config.display_name
        )
        content = content.replace(
            "Codex Python Boilerplate", config.display_name
        )
        content = content.replace(
            BOILERPLATE_REPOSITORY_URL,
            config.repository_url or "",
        )
        owner = config.code_owner or config.author_name
        content = content.replace(
            "[`@EmadHelmi`](https://github.com/EmadHelmi)",
            f"`{owner}`",
        )
        for old, new in replacements:
            content = content.replace(old, new)
        _write_text(path, content)


def _render_private_security_policy(config: SetupConfig) -> str:
    return f"""# Security Policy

## Reporting a Vulnerability

Do not disclose suspected vulnerabilities in a public issue or change
proposal. Send a private report to
[{config.author_email}](mailto:{config.author_email}) with a subject beginning
with `[SECURITY]`.

Include the affected component, realistic impact, reproduction details,
affected versions, and any proposed mitigation. Do not include unrelated
credentials, personal data, or third-party secrets.

The {config.display_name} maintainers will coordinate investigation,
remediation, disclosure, and reporter credit according to project policy.
"""


def _customize_host_files(root: Path, config: SetupConfig) -> None:
    github_test = root / "tests/test_github_pr_policy.py"
    gitlab_test = root / "tests/test_gitlab_mr_policy.py"
    if config.host == "github" and config.collaboration == "collaborative":
        _remove_path(gitlab_test)
    elif config.host == "gitlab" and config.collaboration == "collaborative":
        _remove_path(github_test)
        content = _replace_once(
            _read_text(gitlab_test),
            "VALIDATOR_PATH = (\n"
            '    PROJECT_ROOT / "templates/providers/gitlab/.gitlab/scripts/'
            'validate_mr.py"\n'
            ")",
            'VALIDATOR_PATH = PROJECT_ROOT / ".gitlab/scripts/validate_mr.py"',
            label="GitLab validator test path",
        )
        _write_text(gitlab_test, content)
    else:
        _remove_path(github_test)
        _remove_path(gitlab_test)

    if config.repository_url is None:
        return
    candidates = (
        root / ".github/REPOSITORY_SETTINGS.md",
        root / ".github/pull_request_template.md",
        root / ".gitlab/REPOSITORY_SETTINGS.md",
        root / ".gitlab/merge_request_templates/Default.md",
    )
    for path in candidates:
        if not path.is_file():
            continue
        repository_slug = urlsplit(config.repository_url).path.strip("/")
        content = _read_text(path).replace(
            "EmadHelmi/codex-python-boilerplate",
            repository_slug,
        )
        content = content.replace(
            "this reusable boilerplate", "this project"
        ).replace("the boilerplate", "the project")
        _write_text(path, content)


def _reset_project_docs(root: Path) -> None:
    definition = root / "docs/project/definition.md"
    content = _read_text(definition)
    content = content.replace(
        "This file is the authoritative product definition for a project "
        "created from\nthe boilerplate. Replace every bracketed instruction ",
        "This file is the authoritative product definition. Replace every "
        "bracketed instruction ",
    )
    _write_text(definition, content)

    agent_guide = root / "docs/project/agent-configuration.md"
    content = _read_text(agent_guide)
    content = content.replace("the boilerplate's", "the project's")
    content = content.replace("The boilerplate", "The project")
    content = content.replace("├── customization.md\n", "")
    _write_text(agent_guide, content)

    register = root / "docs/project/decisions/README.md"
    content = _read_text(register)
    table_marker = "## Decision Register\n"
    before, separator, _ = content.partition(table_marker)
    if not separator:
        raise ProjectSetupError("Decision Register section is missing.")
    _write_text(
        register,
        before
        + table_marker
        + "\nNo project-specific decisions have been accepted yet.\n",
    )
    for path in BOILERPLATE_ADRS:
        _remove_path(root / path)


def _handle_license(root: Path, config: SetupConfig) -> None:
    if config.project_license == "mit":
        return
    license_path = root / "LICENSE"
    notice_path = root / "THIRD_PARTY_NOTICES.md"
    if notice_path.exists():
        raise ProjectSetupError("THIRD_PARTY_NOTICES.md already exists.")
    try:
        license_path.replace(notice_path)
    except OSError as error:
        raise ProjectSetupError(
            "Cannot preserve the MIT provenance notice."
        ) from error


def _remove_template_files(root: Path) -> None:
    for path in TEMPLATE_ONLY_PATHS:
        _remove_path(root / path)


def _run_uv_lock(root: Path) -> None:
    try:
        subprocess.run(
            ["uv", "lock"],
            cwd=root,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ProjectSetupError(
            "uv lock failed in the staged setup; the project was not changed."
        ) from error


def _require_clean_git(root: Path) -> None:
    """Require recoverable setup input before any project mutation."""

    try:
        inside = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ProjectSetupError(
            "Apply requires a Git repository with a committed boilerplate "
            "baseline."
        ) from error
    if inside.stdout.strip() != "true" or status.stdout.strip():
        raise ProjectSetupError(
            "Apply requires a clean Git worktree; commit the boilerplate "
            "baseline first."
        )


def _copy_path(source: Path, destination: Path) -> None:
    """Copy one optional file tree while preserving symlinks."""

    if not source.exists() and not source.is_symlink():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir() and not source.is_symlink():
        shutil.copytree(source, destination, symlinks=True)
    else:
        shutil.copy2(source, destination, follow_symlinks=False)


def _copy_project(source: Path, destination: Path) -> None:
    """Create an isolated project copy without local or generated state."""

    shutil.copytree(
        source,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            ".pytest_cache",
            ".ruff_cache",
            ".coverage",
            "__pycache__",
            "dist",
            "build",
        ),
    )


def _publish_paths(source: Path, destination: Path) -> None:
    """Replace only paths owned by one-time project setup."""

    for relative_path in PUBLISH_PATHS:
        target = destination / relative_path
        _remove_path(target)
        _copy_path(source / relative_path, target)


def _apply_in_place(
    root: Path,
    config: SetupConfig,
    *,
    regenerate_lock: bool,
) -> None:
    """Transform an isolated copy after all input validation succeeds."""

    _customize_pyproject(root, config)
    _customize_package(root, config)
    _write_text(root / "README.md", _render_readme(config))
    _materialize_host(root, config)
    _adapt_collaborative_docs(root, config)
    _customize_host_files(root, config)
    _reset_project_docs(root)
    _handle_license(root, config)
    if regenerate_lock:
        _run_uv_lock(root)
    _remove_template_files(root)


def apply_setup(
    root: Path,
    config: SetupConfig,
    *,
    regenerate_lock: bool = True,
) -> tuple[str, ...]:
    """Apply a validated one-time project setup."""

    actions = planned_actions(root, config)
    resolved = root.resolve()
    _require_clean_git(resolved)
    try:
        with tempfile.TemporaryDirectory(prefix="project-setup-") as temporary:
            temporary_root = Path(temporary)
            staged = temporary_root / "staged"
            backup = temporary_root / "backup"
            _copy_project(resolved, staged)
            _apply_in_place(
                staged,
                config,
                regenerate_lock=regenerate_lock,
            )
            backup.mkdir()
            for relative_path in PUBLISH_PATHS:
                _copy_path(resolved / relative_path, backup / relative_path)
            try:
                _publish_paths(staged, resolved)
            except Exception as publish_error:
                try:
                    _publish_paths(backup, resolved)
                except Exception as rollback_error:
                    raise ProjectSetupError(
                        "Publishing setup failed and rollback was incomplete; "
                        "restore the committed baseline with Git."
                    ) from rollback_error
                raise ProjectSetupError(
                    "Publishing setup failed; the committed baseline was "
                    "restored."
                ) from publish_error
    except ProjectSetupError:
        raise
    except OSError as error:
        raise ProjectSetupError(
            "Cannot stage the project setup; the project was not changed."
        ) from error
    return actions


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preview or apply one-time boilerplate customization."
    )
    parser.add_argument(
        "--host", required=True, choices=("github", "gitlab", "neutral")
    )
    parser.add_argument(
        "--collaboration",
        required=True,
        choices=("solo", "collaborative"),
    )
    parser.add_argument("--distribution-name", required=True)
    parser.add_argument("--import-package", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--author-name", required=True)
    parser.add_argument("--author-email", required=True)
    parser.add_argument(
        "--project-license", required=True, choices=("mit", "unset")
    )
    parser.add_argument("--repository-url")
    parser.add_argument("--code-owner")
    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "apply the displayed plan; otherwise leave the repository "
            "unchanged"
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run project setup from the repository root."""

    arguments = _parser().parse_args(argv)
    config = SetupConfig(
        host=arguments.host,
        collaboration=arguments.collaboration,
        distribution_name=arguments.distribution_name,
        import_package=arguments.import_package,
        display_name=arguments.display_name,
        description=arguments.description,
        author_name=arguments.author_name,
        author_email=arguments.author_email,
        project_license=arguments.project_license,
        repository_url=arguments.repository_url,
        code_owner=arguments.code_owner,
    )
    try:
        actions = (
            apply_setup(Path.cwd(), config)
            if arguments.apply
            else planned_actions(Path.cwd(), config)
        )
    except ProjectSetupError as error:
        print(f"project setup failed: {error}", file=sys.stderr)
        return 2

    heading = "Applied changes:" if arguments.apply else "Planned changes:"
    print(heading)
    for action in actions:
        print(f"- {action}")
    if not arguments.apply:
        print("Re-run with --apply to perform these changes.")
    else:
        print("Next steps:")
        print("- deactivate the current virtual environment if it is active")
        print(
            "- the next command replaces .venv; preserve any unrecorded "
            "manual changes first"
        )
        print(
            "- recreate the local environment with the project prompt: "
            f'uv venv --clear --prompt "{config.distribution_name}"'
        )
        print("- synchronize it: uv sync --locked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
