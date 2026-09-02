# ADR-0003: Separate Host and Collaboration Profiles

- Status: `Accepted`
- Date: 2026-09-02

## Context

Projects created from the boilerplate may be hosted on GitHub, GitLab, or
another source-control platform. They may also be maintained by one person or
through a collaborative contribution process. Hosting provider and
collaboration model are independent concerns: a private GitLab project can be
collaborative, while a GitHub project can be maintained by one person.

A single `solo` profile that merely deletes `.github/` would conflate those
concerns. Keeping files for an unselected provider would also be misleading:
configuration could appear active even though the host never evaluates it.

## Decision Drivers

- Keep hosting-specific automation out of projects that cannot execute it.
- Support both individual and collaborative maintenance on every host.
- Preserve the Codex workflow, engineering standards, and local quality gate
  independently of hosting.
- Make generated repository contents deterministic and testable.
- Avoid claiming support for remote settings that repository files cannot
  apply automatically.

## Decision

Project setup uses two independent dimensions:

```text
host:          github | gitlab | neutral
collaboration: solo | collaborative
```

The canonical boilerplate is published with the complete GitHub collaborative
baseline active. The setup command materializes only the selected provider's
files in a derived project:

- `github` keeps GitHub Actions and GitHub repository metadata;
- `gitlab` replaces GitHub-specific files with GitLab CI and GitLab repository
  metadata;
- `neutral` removes both providers' files and retains only provider-neutral
  source-control language and local quality tooling.

The `collaborative` mode retains contribution, governance, support, security,
ownership, and review-policy material appropriate to the selected host. The
`solo` mode removes public collaboration material while retaining host
automation that remains useful to an individually maintained project.

Remote settings such as template status, protected branches, approval rules,
security features, and merge methods are documented as settings blueprints.
The setup command does not mutate remotes or repository history.

GitHub and GitLab template histories are not treated as equivalent. GitHub
creates a new template-based repository with one initial commit. GitLab custom
project templates use project export and import and can retain repository
history. When a fresh GitLab history is required, users create a blank target,
export only the boilerplate working tree, and initialize Git in that new
directory; the source repository is never rewritten.

## Consequences

### Positive

- Every generated project has an explicit, accurate host and collaboration
  model.
- GitLab and neutral projects contain no inactive `.github/` configuration.
- Hosting can evolve without redefining the collaboration model.
- Local Codex behavior and quality checks remain consistent across all six
  combinations.

### Negative

- The boilerplate must maintain and test two provider integrations plus the
  neutral output.
- GitHub and GitLab capabilities are not perfectly symmetrical, so provider
  documentation must describe genuine differences.
- Selecting another profile after finalization requires starting again from a
  fresh template repository.

## Alternatives Considered

### Treat `solo` as Provider-Neutral

This is smaller, but it incorrectly treats a collaborative GitLab project as a
solo project and couples unrelated decisions.

### Maintain Only a GitHub Profile

Users could delete GitHub files manually, but derived GitLab repositories
would be easy to leave in a misleading or partially configured state.

### Provide Fully Interchangeable Provider Features

GitHub and GitLab do not expose identical repository automation and security
features. Pretending their configurations are interchangeable would create a
fragile abstraction and inaccurate documentation.

## References

- [GitHub template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- [Create a GitLab project](https://docs.gitlab.com/user/project/)
- [GitLab custom project templates](https://docs.gitlab.com/user/group/custom_project_templates/)
