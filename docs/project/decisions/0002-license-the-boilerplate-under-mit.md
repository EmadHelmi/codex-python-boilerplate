# ADR-0002: License the Boilerplate Under MIT

- Status: `Accepted`
- Date: 2026-09-01

## Context

The boilerplate is intended to be copied, modified, and reused for other
projects. Without an explicit license, default copyright restrictions would
make those permissions unclear or unavailable to potential users.

The repository needs a license that keeps reuse straightforward while
preserving attribution and a standard warranty disclaimer.

## Decision Drivers

- Permit broad reuse, modification, and redistribution.
- Keep adoption and compliance simple for derived projects.
- Apply to both the Python package and repository documentation.
- Preserve attribution to the copyright holder.
- Avoid imposing copyleft obligations on derived projects.

## Decision

The boilerplate is licensed under the MIT License.

The copyright notice is:

```text
Copyright (c) 2026 Emad Helmi
```

The Python distribution declares the SPDX expression `MIT` and includes the
root `LICENSE` file in built artifacts.

Derived projects must preserve the MIT copyright and permission notice for
copied boilerplate content. They may add project-specific notices or compatible
terms for their own contributions according to their ownership and
distribution requirements.

## Consequences

### Positive

- Users receive explicit permission to use, copy, modify, and redistribute the
  boilerplate.
- The license is short, widely recognized, and simple to preserve.
- Derived projects are not required to use a copyleft license.
- Distribution metadata and source licensing remain aligned.

### Negative

- The MIT License does not provide the more detailed express patent terms of
  Apache-2.0.
- Derived projects must retain the copyright and permission notice for copied
  boilerplate content.

## Alternatives Considered

### Apache License 2.0

Apache-2.0 is permissive and includes explicit patent terms, but it introduces
more detailed attribution and notice requirements than this small boilerplate
needs.

### No Public License

This would suit a proprietary internal template, but it would contradict the
confirmed goal of allowing others to reuse, modify, and distribute the
boilerplate.

## References

- [MIT License](../../../LICENSE)
- [Open Source Initiative: MIT License](https://opensource.org/license/mit)
- [Python project metadata specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
