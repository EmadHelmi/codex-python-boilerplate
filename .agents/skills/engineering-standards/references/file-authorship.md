<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Optional File Authorship

Classification: **BOILERPLATE / REUSABLE PROJECT BASELINE**.

Application: **OPT-IN**. Apply only after a repository explicitly adopts per-file authorship. Git history and the
repository license are the default sources for authorship, provenance, and reuse rights.

## After Explicit Adoption

- Every new human-maintained repository file MUST include author information.
- This includes a new file created by splitting or extracting existing content.
- Do not treat a simple rename or move as new authorship.
- Do not add metadata retroactively to unrelated files during unrelated work.

## Identity

- Preserve existing author information unless the current task explicitly corrects or updates it.
- For a new file, use the effective repository Git identity only when both are configured:

  ```bash
  git config --get user.name
  git config --get user.email
  ```

- If either value is absent, surface the limitation instead of substituting another identity.
- Add a handle only when the convention requires one and repository metadata establishes it.
- Never invent a name, email, username, or handle.
- Do not identify an AI agent as author or co-author unless explicitly required by repository policy.

## Representation and Placement

Use the format's normal valid mechanism, in this order:

1. A standard or schema-defined author field when the format supports one.
2. Otherwise, a valid comment using established syntax.
3. Otherwise, an established adjacent metadata mechanism.

Examples:

```text
Python / Shell / YAML / TOML / Dockerfile
# Author: Name <email> (@handle)

JavaScript / TypeScript / Go / Java / C-like source
// Author: Name <email> (@handle)

SQL
-- Author: Name <email> (@handle)

HTML / XML / Markdown
<!-- Author: Name <email> (@handle) -->
```

- Prefer a standard author field over a redundant comment.
- Place metadata near the beginning while preserving required leading syntax.
- Keep a shebang first and preserve encoding declarations, XML declarations, frontmatter, and other position-sensitive
  content. Put author information at the earliest valid location.
- Follow an established repository placement pattern.

## Validity and Generated Content

- Metadata MUST NOT invalidate syntax or violate a schema.
- Do not add comments to formats that prohibit them or invent an `author` key where the schema does not permit one.
- If in-file authorship is invalid, use an established external mechanism. If none exists, surface the limitation.
- Do not manually inject metadata into lock files, generated artifacts, vendored files, third-party files, compiled or
  binary files, caches, verbatim authoritative copies, or machine-generated files controlled by a generator.
- When a generator supports authorship metadata or templates, configure the generator instead of post-editing output.

## Existing Attribution

- Preserve a more specific repository or format convention.
- Do not create competing author headers.
- When a new file is substantially based on an existing file, preserve legally or historically relevant attribution.
- Per-file metadata does not replace Git history, copyright notices, licenses, or legally required attribution.
