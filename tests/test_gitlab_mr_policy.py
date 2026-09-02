"""Tests for the generated GitLab merge-request metadata policy."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    PROJECT_ROOT / "templates/providers/gitlab/.gitlab/scripts/validate_mr.py"
)
VALID_BODY = """## Summary

Add a focused change.

## Motivation

Keep the project maintainable.

## Testing

Ran the local quality gate.

## Checklist

- [x] Completed.
"""


@pytest.fixture
def validator() -> ModuleType:
    """Load the GitLab validator template."""

    spec = importlib.util.spec_from_file_location(
        "validate_mr", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the GitLab validator.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_valid_merge_request_metadata_is_accepted(
    validator: ModuleType,
) -> None:
    """Accept complete metadata and a conventional title."""

    assert validator.validate_title("feat(setup): add profile") == []
    assert validator.validate_body(VALID_BODY) == []


def test_incomplete_merge_request_metadata_is_rejected(
    validator: ModuleType,
) -> None:
    """Reject an incomplete body and non-conventional title."""

    assert validator.validate_title("Update setup")
    assert validator.validate_body("## Summary\n\nMissing other sections.")


@pytest.mark.parametrize(
    ("body", "expected_error"),
    [
        (
            VALID_BODY.replace("## Motivation", "## Context"),
            "Include exactly one '## Motivation' section.",
        ),
        (
            VALID_BODY.replace(
                "Keep the project maintainable.",
                "<!-- Explain the motivation. -->",
            ),
            "Provide content in the 'Motivation' section.",
        ),
        (
            VALID_BODY.replace("- [x]", "- [ ]"),
            "Resolve every unchecked merge-request checklist item.",
        ),
        (
            VALID_BODY.replace("- [x]", "Completed."),
            "Complete the merge-request checklist.",
        ),
    ],
)
def test_validate_body_rejects_incomplete_templates(
    validator: ModuleType,
    body: str,
    expected_error: str,
) -> None:
    """Reject missing, empty, and unresolved template sections."""

    assert expected_error in validator.validate_body(body)


def test_validate_body_rejects_sections_out_of_order(
    validator: ModuleType,
) -> None:
    """Keep required sections in template order."""

    body = (
        VALID_BODY.replace("## Summary", "## Temporary", 1)
        .replace("## Motivation", "## Summary", 1)
        .replace("## Temporary", "## Motivation", 1)
    )

    assert validator.validate_body(body) == [
        "Keep the required sections in template order."
    ]


def test_main_accepts_valid_metadata(
    validator: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Return success for complete GitLab merge-request metadata."""

    monkeypatch.setenv("CI_MERGE_REQUEST_TITLE", "docs: improve guide")
    monkeypatch.setenv("CI_MERGE_REQUEST_DESCRIPTION", VALID_BODY)

    assert validator.main() == 0
    assert "satisfies" in capsys.readouterr().out


def test_main_rejects_invalid_or_missing_metadata(
    validator: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Return failure for missing variables and invalid metadata."""

    monkeypatch.delenv("CI_MERGE_REQUEST_TITLE", raising=False)
    monkeypatch.delenv("CI_MERGE_REQUEST_DESCRIPTION", raising=False)
    assert validator.main() == 1
    assert "unavailable" in capsys.readouterr().err

    monkeypatch.setenv("CI_MERGE_REQUEST_TITLE", "Update things")
    monkeypatch.setenv("CI_MERGE_REQUEST_DESCRIPTION", "")
    assert validator.main() == 1
    assert "Conventional Commit" in capsys.readouterr().err


def test_module_entrypoint_uses_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercise the executable module boundary."""

    monkeypatch.setenv("CI_MERGE_REQUEST_TITLE", "docs: improve guide")
    monkeypatch.setenv("CI_MERGE_REQUEST_DESCRIPTION", VALID_BODY)
    namespace = {"__name__": "not-main"}

    assert os.environ["CI_MERGE_REQUEST_TITLE"] == "docs: improve guide"
    assert namespace["__name__"] == "not-main"
