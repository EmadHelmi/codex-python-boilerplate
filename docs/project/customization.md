# Customizing the Boilerplate

Use this checklist once, immediately after creating a repository from the
boilerplate and before implementing product behavior. The setup command
automates deterministic repository transformations; product, legal, security,
and operational decisions remain explicit human work.

## 1. Choose Repository Creation and Git History

Prefer a template mechanism over a fork:

- GitHub **Use this template** creates an independent repository with one
  initial commit;
- an approved GitLab custom project template can populate the project, but it
  may copy the template's branches, commits, and tags;
- fork only to contribute back to the boilerplate;
- a normal clone preserves boilerplate history and is acceptable when that
  provenance is wanted.

For a fresh GitLab history, use `git archive` to copy the tracked working tree
into a new directory, run `git init -b main` there, and commit that unchanged
baseline before customization. The setup command requires this clean recovery
point. Commit the customized result separately after reviewing it. Do not
delete or rewrite the source repository's history.

The setup command never deletes `.git`, rewrites commits, changes remotes,
commits, or pushes. Do not rename inherited commits: either keep their history
or create a new repository through a deliberate template/copy workflow.

## 2. Choose the Profile

Hosting and collaboration are independent:

| Host | Files retained or generated |
| :--- | :--- |
| `github` | `.github/` Actions, dependency automation, and GitHub policy |
| `gitlab` | `.gitlab-ci.yml`, `.gitlab/` templates, ownership, and GitLab policy |
| `neutral` | No `.github/`, `.gitlab/`, or provider-specific automation |

| Collaboration | Behavior |
| :--- | :--- |
| `collaborative` | Retains contribution, governance, support, security, ownership, and review policy |
| `solo` | Removes public collaboration material but preserves useful host CI and local tooling |

The six combinations are tested independently. To change a finalized profile,
start again from a fresh template repository instead of attempting a partial
in-place reversal.

## 3. Choose Project Identity

Prepare these values:

| Value | Example | Use |
| :--- | :--- | :--- |
| Distribution name | `example-service` | Packaging and `uv.lock` |
| Import package | `example_service` | `src/`, imports, coverage, and Import Linter |
| Display name | `Example Service` | README and package documentation |
| Description | `Processes example events.` | Package and repository metadata |
| Author | `Example Team` | Package ownership metadata |
| Author email | `team@example.com` | Package ownership metadata |
| Repository URL | `https://host/group/example-service` | Hosted project links |
| Code Owner | `@example-team` | Collaborative host ownership |

Hosted profiles require a repository URL. Hosted collaborative profiles also
require a Code Owner. Neutral profiles reject those provider-specific values.

## 4. Decide License Treatment

Choose explicitly:

- `--project-license mit` keeps the root MIT license and declares the derived
  project under MIT;
- `--project-license unset` moves the inherited notice to
  `THIRD_PARTY_NOTICES.md` and removes project-level MIT metadata.

The second option does not select a new project license. Apply organizational
or legal policy separately, and never delete the inherited third-party notice.

## 5. Preview and Apply

Preview first:

```bash
uv run python scripts/setup_project.py \
  --host gitlab \
  --collaboration collaborative \
  --distribution-name example-service \
  --import-package example_service \
  --display-name "Example Service" \
  --description "Processes example events." \
  --author-name "Example Team" \
  --author-email "team@example.com" \
  --project-license unset \
  --repository-url https://gitlab.example.com/group/example-service \
  --code-owner @example-team
```

Inspect the plan and repeat it with `--apply`. The command:

- validates that it is running against a fresh boilerplate;
- selects one host and one collaboration profile;
- renames the distribution and import package;
- updates package, test, coverage, Import Linter, hook, and project metadata;
- rewrites the README;
- resets the project definition and ADR register;
- preserves the selected license treatment;
- regenerates `uv.lock`; and
- removes one-time setup templates, setup tests, and this checklist.

The command requires a clean Git worktree, performs all transformations and
lock regeneration in an isolated staging directory, and only then publishes
the result. If staging fails, the project remains unchanged. If publishing
fails, setup restores the committed baseline or reports that manual Git
recovery is required.

## 6. Define the Product Manually

Complete `docs/project/definition.md` with confirmed:

- summary, goals, and non-goals;
- functional requirements;
- runtime, hosting, and integration constraints;
- security and data requirements;
- testing and quality requirements;
- deployment and operational requirements;
- known unknowns;
- first useful milestone; and
- project definition of done.

Remove instructional placeholders. Record only accepted decisions that current
or immediately upcoming work needs. Boilerplate ADRs are removed automatically
because they are not project decision history.

## 7. Configure Git and the Hosting Platform

Inspect local configuration and remotes:

```bash
git config --local --list
git remote -v
```

Set repository-local identity or signing only when it should differ from the
user's global configuration. Never copy another project's signing key.

For GitHub, apply `.github/REPOSITORY_SETTINGS.md`. For GitLab, apply
`.gitlab/REPOSITORY_SETTINGS.md`. These blueprints cover protected branches,
required checks, approvals, merge behavior, security features, and secrets.
Remote settings cannot be guaranteed by committed files alone.

Neutral projects must configure their host manually. Keep the terminology and
documentation provider-neutral until a provider-specific baseline is adopted.

## 8. Review the Engineering Baseline

Confirm or deliberately change:

- Python declarations in `.python-version`, `pyproject.toml`, and hosted CI;
- dependencies and package metadata;
- Ruff, Pyright, pytest, coverage, and Import Linter settings;
- optional engineering profiles;
- VS Code settings;
- pre-commit and pre-push hooks; and
- required CI secrets or integrations.

Do not add dependencies or infrastructure merely because they are common.

## 9. Verify the Result

```bash
uv lock --check
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
uv build
```

Then verify manually:

- no boilerplate identity remains in project-owned metadata;
- exactly one provider baseline is present, or none for `neutral`;
- no inactive GitHub integration or repository configuration remains in
  GitLab or neutral output (dependency source URLs may still point to GitHub);
- no GitLab references remain in GitHub or neutral configuration;
- product definition contains no misleading example requirements;
- license and provenance match the selected policy;
- local Git identity, remote, and optional signing are correct; and
- remote repository settings match the committed blueprint.
