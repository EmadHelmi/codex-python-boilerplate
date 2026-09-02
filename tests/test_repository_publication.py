"""Validate the canonical GitHub publication baseline."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/EmadHelmi/codex-python-boilerplate"
REQUIRED_CHECKS = {
    "Compatibility gate",
    "Quality gate",
    "Review dependency changes",
    "Validate metadata",
}
UV_VERSION_PATTERN = re.compile(
    r'^\s*UV_VERSION:\s*"(?P<version>[^\"]+)"$', re.MULTILINE
)
UV_HOOK_PATTERN = re.compile(
    r"repo: https://github\.com/astral-sh/uv-pre-commit\s+"
    r"rev: (?P<version>\S+)",
)
UV_PRE_COMMIT_DEPENDENCY = "https://github.com/astral-sh/uv-pre-commit"


def load_ruleset() -> dict[str, Any]:
    """Return the versioned default-branch ruleset."""

    path = PROJECT_ROOT / ".github/rulesets/main.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _required_match(pattern: re.Pattern[str], content: str) -> str:
    match = pattern.search(content)
    assert match is not None
    return match.group("version")


def test_uv_runtime_and_lock_hook_versions_match() -> None:
    """Prevent CI uv from drifting behind the lock hook."""

    workflow = (PROJECT_ROOT / ".github/workflows/ci.yml").read_text(
        encoding="utf-8"
    )
    hooks = (PROJECT_ROOT / ".pre-commit-config.yaml").read_text(
        encoding="utf-8"
    )
    assert _required_match(UV_VERSION_PATTERN, workflow) == _required_match(
        UV_HOOK_PATTERN, hooks
    )


def test_dependabot_does_not_split_the_coupled_uv_update() -> None:
    """Keep CI and hook uv upgrades in one manually reviewed change."""

    dependabot = (PROJECT_ROOT / ".github/dependabot.yml").read_text(
        encoding="utf-8"
    )
    assert "ignore:" in dependabot
    assert f"dependency-name: {UV_PRE_COMMIT_DEPENDENCY}" in dependabot


def test_packaging_metadata_uses_canonical_repository_urls() -> None:
    """Keep public package links aligned with this repository."""

    with (PROJECT_ROOT / "pyproject.toml").open("rb") as file:
        project = tomllib.load(file)["project"]
    assert project["urls"] == {
        "Documentation": f"{REPOSITORY_URL}/tree/main/docs",
        "Issues": f"{REPOSITORY_URL}/issues",
        "Repository": REPOSITORY_URL,
    }


def test_ruleset_and_workflows_use_the_same_required_checks() -> None:
    """Keep protected-branch status checks executable."""

    rules = {rule["type"]: rule for rule in load_ruleset()["rules"]}
    parameters = rules["required_status_checks"]["parameters"]
    assert {
        check["context"] for check in parameters["required_status_checks"]
    } == REQUIRED_CHECKS
    assert parameters["strict_required_status_checks_policy"] is True
    assert parameters["do_not_enforce_on_create"] is False


def test_github_actions_are_pinned_to_commit_shas() -> None:
    """Prevent mutable action tags in privileged repository automation."""

    action_pattern = re.compile(
        r"^\s*uses:\s*[^\s]+@(?P<ref>[^\s]+)", re.MULTILINE
    )
    for workflow in (PROJECT_ROOT / ".github/workflows").glob("*.yml"):
        content = workflow.read_text(encoding="utf-8")
        references = action_pattern.findall(content)
        assert references
        assert all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in references)


def test_gitlab_ci_installs_git_before_running_pre_commit() -> None:
    """Keep the slim GitLab runner compatible with repository hooks."""

    pipeline = (
        PROJECT_ROOT / "templates/providers/gitlab/.gitlab-ci.yml"
    ).read_text(encoding="utf-8")
    install = "apt-get install --yes --no-install-recommends git"
    assert install in pipeline
    assert "git --version" in pipeline
    assert pipeline.index(install) < pipeline.index("uv sync --locked")
