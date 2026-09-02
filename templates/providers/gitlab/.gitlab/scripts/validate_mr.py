"""Validate GitLab merge-request metadata."""

from __future__ import annotations

import os
import re
import sys

MAX_TITLE_LENGTH = 100
TITLE_PATTERN = re.compile(
    r"^(?:build|chore|ci|docs|feat|fix|perf|refactor|revert|test)"
    r"(?:\([a-z0-9][a-z0-9._/-]*\))?!?: [^\s].*$"
)
REQUIRED_SECTIONS = ("Summary", "Motivation", "Testing", "Checklist")
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
UNCHECKED_ITEM_PATTERN = re.compile(r"^\s*-\s*\[\s\]", re.MULTILINE)
CHECKED_ITEM_PATTERN = re.compile(r"^\s*-\s*\[[xX]\]", re.MULTILINE)


def validate_title(title: str) -> list[str]:
    """Return policy errors for a merge-request title."""

    errors: list[str] = []
    if len(title) > MAX_TITLE_LENGTH:
        errors.append(
            f"The title must not exceed {MAX_TITLE_LENGTH} characters."
        )
    if TITLE_PATTERN.fullmatch(title) is None:
        errors.append(
            "Use a Conventional Commit title such as "
            "'feat(scope): describe the change'."
        )
    return errors


def _visible_content(lines: list[str]) -> str:
    return HTML_COMMENT_PATTERN.sub("", "\n".join(lines)).strip()


def validate_body(body: str) -> list[str]:
    """Return policy errors for a merge-request description."""

    lines = body.splitlines()
    locations: list[tuple[str, int]] = []
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        marker = f"## {section}"
        matches = [
            index for index, line in enumerate(lines) if line.strip() == marker
        ]
        if len(matches) != 1:
            errors.append(f"Include exactly one '{marker}' section.")
        else:
            locations.append((section, matches[0]))

    if errors:
        return errors
    if [index for _, index in locations] != sorted(
        index for _, index in locations
    ):
        return ["Keep the required sections in template order."]

    for position, (section, start) in enumerate(locations):
        end = (
            locations[position + 1][1]
            if position + 1 < len(locations)
            else len(lines)
        )
        content = _visible_content(lines[start + 1 : end])
        if section != "Checklist" and not content:
            errors.append(f"Provide content in the '{section}' section.")
        if section == "Checklist":
            if CHECKED_ITEM_PATTERN.search(content) is None:
                errors.append("Complete the merge-request checklist.")
            if UNCHECKED_ITEM_PATTERN.search(content) is not None:
                errors.append(
                    "Resolve every unchecked merge-request checklist item."
                )
    return errors


def main() -> int:
    """Validate the merge request described by GitLab CI variables."""

    title = os.environ.get("CI_MERGE_REQUEST_TITLE")
    body = os.environ.get("CI_MERGE_REQUEST_DESCRIPTION")
    if title is None or body is None:
        print(
            "MR policy: merge-request variables are unavailable.",
            file=sys.stderr,
        )
        return 1

    errors = [*validate_title(title), *validate_body(body)]
    if errors:
        for error in errors:
            print(f"MR policy: {error}", file=sys.stderr)
        return 1

    print("Merge-request metadata satisfies the contribution policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
