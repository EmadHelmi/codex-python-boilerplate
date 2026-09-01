<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Rule Governance and Compatibility

Classification: **HYBRID** for compatibility baselines and **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL** for compliance.

Application: Read for any task that applies repository engineering standards.

## Compliance

- Follow every rule applicable to the current change. Never silently violate an applicable rule.
- Apply rules according to their actual scope. When applicable rules overlap, prefer the narrower and more specific
  rule for the concern being addressed.
- Treat an explicit repository- or project-specific rule as an intentional specialization of a reusable generic rule
  when both govern the same concern.
- Do not infer precedence from filenames, directory ordering, or numeric prefixes.
- If applicable rules remain materially incompatible after considering scope, surface the conflict rather than
  silently choosing one.
- Apply compliance checks proportionally. Do not perform a repository-wide audit for a local edit unless the task or
  an explicit compliance workflow requires one.
- Apply the compatibility policy below before relying on version-sensitive guidance.
- If the repository provides an explicit compliance or exception-recording workflow, use it when a violation must be
  intentionally accepted or deferred.

## Classification Model

| Classification | Meaning |
| :--- | :--- |
| **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL** | Guidance independent of a project or company and suitable as a reusable baseline |
| **BOILERPLATE / REUSABLE PROJECT BASELINE** | A deliberate reusable default that does not claim universal authority |
| **PERSONAL CONVENTION** | An individual's preference, usable only when compatible with authoritative requirements |
| **PROJECT-SPECIFIC / COMPANY-SPECIFIC** | Guidance whose meaning depends on one repository, product, or organization |
| **HYBRID** | A project-neutral principle delivered through a concrete implementation selected by the baseline |

Classification describes where a rule gets its authority and how safely it can be reused. File placement is only for
discovery. When classifying a new standard, use the narrowest accurate classification:

1. Use **PROJECT-SPECIFIC / COMPANY-SPECIFIC** when the rule depends on a repository, product, or organization.
2. Use **PERSONAL CONVENTION** when it expresses an individual's preferred style.
3. Use **BOILERPLATE / REUSABLE PROJECT BASELINE** for a reusable default selected by this project base.
4. Use **HYBRID** when a project-neutral principle is coupled to a selected concrete implementation.
5. Use **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL** only when the rule genuinely has no project, company, or baseline
   dependency.

When standards overlap, use this order:

1. Follow explicit repository and organization requirements within their scope.
2. Treat boilerplate and hybrid rules as selected defaults, not universal standards.
3. Apply general rules where a more specific requirement does not specialize them.
4. Never let a personal convention override correctness or an authoritative requirement.
5. Surface material conflicts instead of choosing silently.

## Organization and Applicability

- Organize standards by engineering concern only to help discovery. Directory and filename order do not establish
  classification, applicability, or precedence.
- Record each standard's classification and applicability in its routed reference.
- Use the narrowest routing that reliably loads a standard when needed:
  - route small cross-cutting policies from the skill for arbitrary engineering work;
  - route file-format standards only for matching files or tasks;
  - load detailed concern-specific guidance intelligently when its subject is involved;
  - require deliberate invocation for optional profiles.
- Keep human navigation concise and do not duplicate normative rule text across inventory documents.
- Codex-native references MUST use explicit classification and routing instead of depending on filename conventions.

## Compatibility Policy

- Treat versions declared by the current project as authoritative. Inspect `pyproject.toml`, lock files, framework
  configuration, and other dependency metadata when behavior depends on a language, framework, library, or tool.
- Treat the reviewed versions below as documentation and behavior baselines, not dependency requirements.
- Before applying version-sensitive guidance, compare the project's declared version with the reviewed baseline.
- For an older project version, do not use APIs or behavior that may have been introduced later without verifying
  availability in the actual version.
- For a newer major or minor version, do not assume version-sensitive rules remain current. Verify affected behavior
  against current official documentation when practical and mention when the relevant rule area may need review.
- Do not warn about unrelated compatibility concerns or a newer patch release unless the patch materially changes the
  behavior in question.

## Reviewed Baselines

| Rule area | Reviewed baseline | Reviewed on |
| :--- | :---: | :---: |
| Python language and standard library | 3.14.7 | 2026-08-20 |
| uv | 0.12.x | 2026-08-20 |
| Ruff | 0.16.5 | 2026-09-01 |
| Pyright | 1.1.411 | 2026-08-20 |
| pytest | 9.1.1 | 2026-08-20 |
| pytest-django | 4.14.0 | 2026-08-20 |
| Django | 6.1 | 2026-08-20 |
| Django REST Framework | 3.18.0 | 2026-08-20 |
| Import Linter | 2.13 | 2026-08-20 |

Update a baseline only after reviewing the corresponding rule area against that version. A baseline update is not a
dependency upgrade.
