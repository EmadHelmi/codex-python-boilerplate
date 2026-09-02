# Getting Started

This guide takes a fresh boilerplate repository to a customized and verified
project without carrying unrelated hosting configuration. Git-history behavior
depends on the creation method and hosting platform described below.

## Prerequisites

Install Git, Python 3.14, and [uv](https://docs.astral.sh/uv/). Node.js is not a
project prerequisite; pre-commit provisions the runtime required by the pinned
Markdown hook.

## Create the Repository

### GitHub

Use **Use this template** for an independent project. A repository created from
a GitHub template starts with its own initial commit. Fork only when the goal
is to contribute back to the boilerplate.

### GitLab

GitLab custom project templates can copy branches, commits, and tags through
project export and import. Use that workflow only when inherited history is
acceptable.

For an independent history, export the tracked tree into a new directory and
initialize the new repository there:

```bash
mkdir ../example-service
git archive HEAD | tar -x -C ../example-service
cd ../example-service
git init -b main
git add .
git commit -m "Initialize from codex-python-boilerplate"
```

The committed baseline gives setup a recovery point. The command refuses to
apply changes while the worktree is dirty. This flow does not delete or rewrite
the boilerplate repository's `.git` directory.

### Other Hosts

Create the repository using the host's template or repository-copy mechanism.
Select `neutral` during setup so GitHub and GitLab files are removed.

## Create the Environment

```bash
uv sync --locked
```

## Preview Project Setup

The setup command combines two independent choices:

- `--host github|gitlab|neutral` selects hosted automation;
- `--collaboration solo|collaborative` selects contribution infrastructure.

It also requires explicit project identity, authorship, and license treatment.
Run the example in the root README without `--apply`, inspect every reported
action, and then apply the same command explicitly.

`--project-license mit` keeps the root MIT license as the new project's
license. `--project-license unset` removes the project-level license metadata
and preserves the boilerplate license as `THIRD_PARTY_NOTICES.md`; the project
owner must then select its own license according to applicable policy.

The command customizes project files, regenerates `uv.lock`, and removes its
one-time templates and tests. It never commits, rewrites history, changes a
remote, or pushes.

## Complete the Manual Steps

After setup:

1. complete `docs/project/definition.md`;
2. decide only technical questions required for the first useful milestone;
3. configure repository-local Git identity and signing when required;
4. apply the selected host's documented remote settings;
5. add only required CI secrets and integrations;
6. install local hooks; and
7. run the complete verification.

```bash
git config --local --list
git remote -v
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
uv lock --check
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
uv build
```

For all identity fields, manual decisions, provider behavior, and completion
criteria, follow the [customization guide](project/customization.md).
