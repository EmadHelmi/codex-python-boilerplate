"""Tests for one-time project setup and all supported profile combinations."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from types import ModuleType

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETUP_PATH = PROJECT_ROOT / "scripts/setup_project.py"
COMMUNITY_FILES = (
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "SECURITY.md",
    "SUPPORT.md",
)


def load_setup_module() -> ModuleType:
    """Load the setup command as an importable module."""

    spec = importlib.util.spec_from_file_location("setup_project", SETUP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the project setup module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def setup_project(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """Return a freshly loaded setup module."""

    module = load_setup_module()
    monkeypatch.setattr(module, "_require_clean_git", lambda _root: None)
    return module


@pytest.fixture
def template_root(tmp_path: Path) -> Path:
    """Copy the real template without local or Git state."""

    target = tmp_path / "project"
    shutil.copytree(
        PROJECT_ROOT,
        target,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            ".pytest_cache",
            ".ruff_cache",
            ".coverage",
            "__pycache__",
            "dist",
        ),
    )
    return target


def make_config(
    setup_project: ModuleType,
    *,
    host: str,
    collaboration: str,
    project_license: str = "mit",
) -> object:
    """Create one complete configuration for a requested profile."""

    hosted = host != "neutral"
    return setup_project.SetupConfig(
        host=host,
        collaboration=collaboration,
        distribution_name="example-service",
        import_package="example_service",
        display_name="Example Service",
        description="Processes example events.",
        author_name="Example Team",
        author_email="team@example.com",
        project_license=project_license,
        repository_url=(
            f"https://{host}.example.com/group/example-service"
            if hosted
            else None
        ),
        code_owner=(
            "@example-team"
            if hosted and collaboration == "collaborative"
            else None
        ),
    )


def snapshot(root: Path) -> dict[str, bytes]:
    """Capture repository files for a preview-mutation assertion."""

    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_preview_reports_actions_without_mutation(
    setup_project: ModuleType,
    template_root: Path,
) -> None:
    """Keep preview mode read-only."""

    before = snapshot(template_root)
    config = make_config(
        setup_project,
        host="github",
        collaboration="collaborative",
    )

    actions = setup_project.planned_actions(template_root, config)

    assert actions[0] == "select github/collaborative profile"
    assert snapshot(template_root) == before


@pytest.mark.parametrize(
    ("host", "collaboration"),
    [
        ("github", "collaborative"),
        ("github", "solo"),
        ("gitlab", "collaborative"),
        ("gitlab", "solo"),
        ("neutral", "collaborative"),
        ("neutral", "solo"),
    ],
)
def test_apply_produces_exact_profile_and_project_identity(
    setup_project: ModuleType,
    template_root: Path,
    host: str,
    collaboration: str,
) -> None:
    """Generate each host and collaboration combination without residue."""

    config = make_config(
        setup_project,
        host=host,
        collaboration=collaboration,
    )

    setup_project.apply_setup(
        template_root,
        config,
        regenerate_lock=False,
    )

    assert (template_root / "src/example_service/__init__.py").is_file()
    assert not (template_root / "src/codex_boilerplate").exists()
    assert not (template_root / "scripts/setup_project.py").exists()
    assert not (template_root / "templates").exists()
    assert not (template_root / "docs/project/customization.md").exists()
    assert all(
        not (template_root / path).exists()
        for path in setup_project.BOILERPLATE_ADRS
    )

    pyproject = (template_root / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "example-service"' in pyproject
    assert 'module-name = "example_service"' in pyproject
    assert 'root_package = "example_service"' in pyproject
    assert "codex-python-boilerplate" not in pyproject

    assert (template_root / ".github").exists() is (host == "github")
    assert (template_root / ".gitlab").exists() is (host == "gitlab")
    assert (template_root / ".gitlab-ci.yml").exists() is (host == "gitlab")

    for path in COMMUNITY_FILES:
        assert (template_root / path).exists() is (
            collaboration == "collaborative"
        )

    if collaboration == "collaborative" and host == "github":
        assert "@example-team" in (
            template_root / ".github/CODEOWNERS"
        ).read_text(encoding="utf-8")
        assert (template_root / "tests/test_github_pr_policy.py").is_file()
        assert not (template_root / "tests/test_gitlab_mr_policy.py").exists()
    if collaboration == "collaborative" and host == "gitlab":
        assert "@example-team" in (
            template_root / ".gitlab/CODEOWNERS"
        ).read_text(encoding="utf-8")
        gitlab_test = template_root / "tests/test_gitlab_mr_policy.py"
        assert gitlab_test.is_file()
        assert not (template_root / "tests/test_github_pr_policy.py").exists()
        assert "templates/providers" not in gitlab_test.read_text(
            encoding="utf-8"
        )
    if collaboration == "solo" and host == "github":
        assert (template_root / ".github/workflows/ci.yml").is_file()
        settings = template_root / ".github/REPOSITORY_SETTINGS.md"
        assert settings.is_file()
        assert "Quality gate" in settings.read_text(encoding="utf-8")
        assert "mandatory reviewer" in settings.read_text(encoding="utf-8")
        assert not (template_root / ".github/CODEOWNERS").exists()
        assert not (template_root / ".github/workflows/pr-policy.yml").exists()
    if collaboration == "solo" and host == "gitlab":
        ci = (template_root / ".gitlab-ci.yml").read_text(encoding="utf-8")
        assert "quality:" in ci
        assert "validate-metadata:" not in ci
        settings = template_root / ".gitlab/REPOSITORY_SETTINGS.md"
        assert settings.is_file()
        assert "quality" in settings.read_text(encoding="utf-8")
        assert "mandatory reviewer" in settings.read_text(encoding="utf-8")
    if collaboration == "solo" or host == "neutral":
        assert not (template_root / "tests/test_github_pr_policy.py").exists()
        assert not (template_root / "tests/test_gitlab_mr_policy.py").exists()

    identity_paths = [
        template_root / "README.md",
        template_root / "pyproject.toml",
        template_root / "docs/project/agent-configuration.md",
    ]
    identity_paths.extend(
        template_root / path
        for path in COMMUNITY_FILES
        if (template_root / path).is_file()
    )
    identity_text = "\n".join(
        path.read_text(encoding="utf-8") for path in identity_paths
    ).casefold()
    if host == "gitlab":
        assert "github" not in identity_text
    if host == "neutral":
        assert "github" not in identity_text
        assert "gitlab" not in identity_text


def test_unset_license_preserves_provenance_without_project_license(
    setup_project: ModuleType,
    template_root: Path,
) -> None:
    """Keep the inherited notice without silently licensing derived work."""

    config = make_config(
        setup_project,
        host="neutral",
        collaboration="solo",
        project_license="unset",
    )

    setup_project.apply_setup(
        template_root,
        config,
        regenerate_lock=False,
    )

    assert not (template_root / "LICENSE").exists()
    assert (template_root / "THIRD_PARTY_NOTICES.md").is_file()
    pyproject = (template_root / "pyproject.toml").read_text(encoding="utf-8")
    assert 'license = "MIT"' not in pyproject
    assert 'license-files = ["THIRD_PARTY_NOTICES.md"]' in pyproject


def test_unset_license_notice_is_in_built_artifacts(
    setup_project: ModuleType,
    template_root: Path,
    tmp_path: Path,
) -> None:
    """Ship inherited MIT provenance in both wheel and source artifacts."""

    config = make_config(
        setup_project,
        host="neutral",
        collaboration="solo",
        project_license="unset",
    )
    setup_project.apply_setup(
        template_root,
        config,
        regenerate_lock=False,
    )
    artifacts = tmp_path / "artifacts"
    subprocess.run(
        [
            "uv",
            "build",
            "--offline",
            "--out-dir",
            str(artifacts),
        ],
        cwd=template_root,
        check=True,
    )

    wheel = next(artifacts.glob("*.whl"))
    source = next(artifacts.glob("*.tar.gz"))
    with zipfile.ZipFile(wheel) as archive:
        assert any(
            Path(name).name == "THIRD_PARTY_NOTICES.md"
            for name in archive.namelist()
        )
    with tarfile.open(source) as archive:
        assert any(
            Path(name).name == "THIRD_PARTY_NOTICES.md"
            for name in archive.getnames()
        )


def test_apply_rejects_second_customization(
    setup_project: ModuleType,
    template_root: Path,
) -> None:
    """Fail clearly instead of partially applying setup twice."""

    config = make_config(
        setup_project,
        host="github",
        collaboration="solo",
    )
    setup_project.apply_setup(
        template_root,
        config,
        regenerate_lock=False,
    )

    with pytest.raises(
        setup_project.ProjectSetupError,
        match="fresh boilerplate",
    ):
        setup_project.planned_actions(template_root, config)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("distribution_name", "Bad Name", "Distribution name"),
        ("import_package", "bad-package", "Python identifier"),
        ("author_email", "invalid", "Author email"),
    ],
)
def test_config_rejects_invalid_identity(
    setup_project: ModuleType,
    field: str,
    value: str,
    message: str,
) -> None:
    """Reject invalid identity before filesystem mutation."""

    values = {
        "host": "github",
        "collaboration": "collaborative",
        "distribution_name": "example-service",
        "import_package": "example_service",
        "display_name": "Example Service",
        "description": "Processes example events.",
        "author_name": "Example Team",
        "author_email": "team@example.com",
        "project_license": "mit",
        "repository_url": "https://github.example/example-service",
        "code_owner": "@example-team",
    }
    values[field] = value
    config = setup_project.SetupConfig(**values)

    with pytest.raises(setup_project.ProjectSetupError, match=message):
        setup_project.validate_config(config)


def test_neutral_rejects_provider_values(setup_project: ModuleType) -> None:
    """Keep neutral output free from provider identity."""

    config = setup_project.SetupConfig(
        host="neutral",
        collaboration="solo",
        distribution_name="example-service",
        import_package="example_service",
        display_name="Example Service",
        description="Processes example events.",
        author_name="Example Team",
        author_email="team@example.com",
        project_license="mit",
        repository_url="https://example.com/project",
        code_owner=None,
    )

    with pytest.raises(
        setup_project.ProjectSetupError,
        match="Neutral projects",
    ):
        setup_project.validate_config(config)


def test_hosted_collaboration_requires_repository_and_owner(
    setup_project: ModuleType,
) -> None:
    """Reject incomplete hosted identity before touching files."""

    base = {
        "host": "github",
        "collaboration": "collaborative",
        "distribution_name": "example-service",
        "import_package": "example_service",
        "display_name": "Example Service",
        "description": "Processes example events.",
        "author_name": "Example Team",
        "author_email": "team@example.com",
        "project_license": "mit",
        "repository_url": None,
        "code_owner": None,
    }
    with pytest.raises(
        setup_project.ProjectSetupError,
        match="repository-url",
    ):
        setup_project.validate_config(setup_project.SetupConfig(**base))

    base["repository_url"] = "https://github.example/example-service"
    with pytest.raises(
        setup_project.ProjectSetupError,
        match="code-owner",
    ):
        setup_project.validate_config(setup_project.SetupConfig(**base))

    base["code_owner"] = "example-team"
    with pytest.raises(
        setup_project.ProjectSetupError,
        match="@user",
    ):
        setup_project.validate_config(setup_project.SetupConfig(**base))


@pytest.mark.parametrize(
    ("host", "url", "message"),
    [
        ("github", "http://github.com/team/project", "safe HTTPS"),
        ("github", "https://gitlab.com/team/project", "conflicts"),
        ("gitlab", "https://github.com/team/project", "conflicts"),
        ("gitlab", "https://gitlab.example/team/project?x=1", "safe HTTPS"),
        ("gitlab", "https://gitlab.example/team/project\nnext", "safe HTTPS"),
    ],
)
def test_config_rejects_unsafe_or_mismatched_repository_url(
    setup_project: ModuleType,
    host: str,
    url: str,
    message: str,
) -> None:
    """Reject malformed URLs and obvious provider mismatches."""

    config = make_config(
        setup_project,
        host=host,
        collaboration="collaborative",
    )
    config = setup_project.SetupConfig(
        **{**config.__dict__, "repository_url": url}
    )
    with pytest.raises(setup_project.ProjectSetupError, match=message):
        setup_project.validate_config(config)


@pytest.mark.parametrize(
    "owner", ["@group name", "@group//team", "@group/", "@bad\nowner"]
)
def test_config_rejects_unsafe_code_owner(
    setup_project: ModuleType,
    owner: str,
) -> None:
    """Keep generated ownership files to one syntactically safe principal."""

    config = make_config(
        setup_project,
        host="github",
        collaboration="collaborative",
    )
    config = setup_project.SetupConfig(
        **{**config.__dict__, "code_owner": owner}
    )
    with pytest.raises(setup_project.ProjectSetupError, match="@user"):
        setup_project.validate_config(config)


def test_generated_provider_urls_use_native_routes(
    setup_project: ModuleType,
    template_root: Path,
) -> None:
    """Use GitHub and GitLab's distinct documentation and issue routes."""

    config = make_config(
        setup_project,
        host="gitlab",
        collaboration="solo",
    )
    setup_project.apply_setup(template_root, config, regenerate_lock=False)
    pyproject = (template_root / "pyproject.toml").read_text(encoding="utf-8")
    assert (
        "https://gitlab.example.com/group/example-service/-/tree/main/docs"
        in pyproject
    )
    assert (
        "https://gitlab.example.com/group/example-service/-/issues"
        in pyproject
    )


def test_config_rejects_keyword_and_unsafe_toml_text(
    setup_project: ModuleType,
) -> None:
    """Reject values that would produce invalid Python or TOML."""

    config = setup_project.SetupConfig(
        host="neutral",
        collaboration="solo",
        distribution_name="example-service",
        import_package="class",
        display_name="Example Service",
        description="Processes example events.",
        author_name="Example Team",
        author_email="team@example.com",
        project_license="mit",
        repository_url=None,
        code_owner=None,
    )
    with pytest.raises(setup_project.ProjectSetupError, match="keyword"):
        setup_project.validate_config(config)

    invalid_text = setup_project.SetupConfig(
        **{
            **config.__dict__,
            "import_package": "example",
            "description": 'bad"',
        }
    )
    with pytest.raises(setup_project.ProjectSetupError, match="description"):
        setup_project.validate_config(invalid_text)


def test_helpers_report_invalid_or_inaccessible_filesystem_state(
    setup_project: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate low-level filesystem failures into setup errors."""

    with pytest.raises(setup_project.ProjectSetupError, match="Cannot read"):
        setup_project._read_text(tmp_path / "missing")
    with pytest.raises(setup_project.ProjectSetupError, match="Cannot write"):
        setup_project._write_text(tmp_path, "content")

    target = tmp_path / "target"
    target.write_text("content", encoding="utf-8")

    def fail_unlink(_path: Path) -> None:
        raise OSError("denied")

    monkeypatch.setattr(Path, "unlink", fail_unlink)
    with pytest.raises(setup_project.ProjectSetupError, match="Cannot remove"):
        setup_project._remove_path(target)


def test_transform_helpers_reject_ambiguous_content(
    setup_project: ModuleType,
) -> None:
    """Reject unsafe replacement, marker, and TOML table states."""

    with pytest.raises(setup_project.ProjectSetupError, match="found 0"):
        setup_project._replace_once("content", "missing", "new", label="item")
    with pytest.raises(setup_project.ProjectSetupError, match="marker"):
        setup_project._without_marked_section("content", "start", "end")
    assert setup_project._remove_toml_table(
        "[project]\n", "[project.urls]"
    ) == ("[project]\n")
    duplicate = "[project.urls]\na = 1\n[project.urls]\nb = 2\n"
    with pytest.raises(setup_project.ProjectSetupError, match="ambiguous"):
        setup_project._remove_toml_table(duplicate, "[project.urls]")


def test_package_setup_rejects_existing_target(
    setup_project: ModuleType,
    template_root: Path,
) -> None:
    """Avoid overwriting an existing import package."""

    (template_root / "src/example_service").mkdir()
    config = make_config(
        setup_project,
        host="neutral",
        collaboration="solo",
    )
    with pytest.raises(
        setup_project.ProjectSetupError, match="already exists"
    ):
        setup_project._customize_package(template_root, config)


def test_uv_lock_success_and_failure_are_reported(
    setup_project: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Run uv lock and translate an unavailable command into setup context."""

    calls: list[tuple[list[str], Path]] = []

    def succeed(command: list[str], *, cwd: Path, check: bool) -> None:
        assert check is True
        calls.append((command, cwd))

    monkeypatch.setattr(subprocess, "run", succeed)
    setup_project._run_uv_lock(tmp_path)
    assert calls == [(["uv", "lock"], tmp_path)]

    def fail(command: list[str], *, cwd: Path, check: bool) -> None:
        raise subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(subprocess, "run", fail)
    with pytest.raises(
        setup_project.ProjectSetupError, match="uv lock failed"
    ):
        setup_project._run_uv_lock(tmp_path)


def test_cli_previews_and_reports_invalid_configuration(
    setup_project: ModuleType,
    template_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Keep the command preview-first and return a stable setup error."""

    monkeypatch.chdir(template_root)
    arguments = [
        "--host",
        "neutral",
        "--collaboration",
        "solo",
        "--distribution-name",
        "example-service",
        "--import-package",
        "example_service",
        "--display-name",
        "Example Service",
        "--description",
        "Processes example events.",
        "--author-name",
        "Example Team",
        "--author-email",
        "team@example.com",
        "--project-license",
        "mit",
    ]
    assert setup_project.main(arguments) == 0
    output = capsys.readouterr().out
    assert "Planned changes:" in output
    assert "Re-run with --apply" in output

    arguments[arguments.index("example_service")] = "bad-package"
    assert setup_project.main(arguments) == 2
    assert "project setup failed" in capsys.readouterr().err


def test_apply_with_lock_regeneration_uses_runner(
    setup_project: ModuleType,
    template_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regenerate the lockfile in normal apply mode."""

    called: list[Path] = []

    def record_lock(root: Path) -> None:
        called.append(root)

    monkeypatch.setattr(
        setup_project,
        "_run_uv_lock",
        record_lock,
    )
    config = make_config(
        setup_project,
        host="neutral",
        collaboration="solo",
    )
    setup_project.apply_setup(template_root, config)
    assert len(called) == 1
    assert called[0] != template_root.resolve()
    assert called[0].name == "staged"


def test_apply_requires_clean_git_worktree(
    template_root: Path,
) -> None:
    """Refuse destructive setup without a committed recovery point."""

    module = load_setup_module()
    config = make_config(module, host="neutral", collaboration="solo")
    before = snapshot(template_root)
    with pytest.raises(module.ProjectSetupError, match="Git repository"):
        module.apply_setup(template_root, config, regenerate_lock=False)
    assert snapshot(template_root) == before


def test_staging_failure_leaves_project_unchanged(
    setup_project: ModuleType,
    template_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Perform all fallible transformation work outside the real project."""

    config = make_config(
        setup_project,
        host="github",
        collaboration="collaborative",
    )
    before = snapshot(template_root)

    def fail_after_staged_write(
        root: Path,
        _config: object,
        *,
        regenerate_lock: bool,
    ) -> None:
        assert regenerate_lock is False
        (root / "README.md").write_text("partial", encoding="utf-8")
        raise setup_project.ProjectSetupError("staged failure")

    monkeypatch.setattr(
        setup_project, "_apply_in_place", fail_after_staged_write
    )
    with pytest.raises(
        setup_project.ProjectSetupError, match="staged failure"
    ):
        setup_project.apply_setup(
            template_root,
            config,
            regenerate_lock=False,
        )
    assert snapshot(template_root) == before
