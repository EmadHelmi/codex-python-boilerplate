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

## Create the Initial Environment

```bash
uv sync --locked
```

This environment initially carries the boilerplate prompt. Project setup
cannot safely replace an environment while its Python process is running, so a
later step recreates it with the new distribution name.

## Preview Project Setup

The setup command combines two independent choices:

- `--host github|gitlab|neutral` selects hosted automation;
- `--collaboration solo|collaborative` selects contribution infrastructure.

It also requires explicit project identity, authorship, and license treatment.
The author fields populate Python package metadata and generated project
documents; they do not configure Git identity.

Preview setup first. This GitLab solo example intentionally omits
`--repository-url`; repository links may be added to the resulting project
metadata after the remote repository exists:

```bash
uv run python scripts/setup_project.py \
  --host gitlab \
  --collaboration solo \
  --distribution-name example-service \
  --import-package example_service \
  --display-name "Example Service" \
  --description "Processes example events." \
  --author-name "Example Team" \
  --author-email "team@example.com" \
  --project-license mit
```

Inspect every reported action, then repeat the same command with `--apply`.
Collaborative GitHub and GitLab projects additionally require
`--repository-url` and `--code-owner`. A repository URL only populates package
metadata and generated links; setup never creates a remote repository or
changes a Git remote.

`--project-license mit` keeps the root MIT license as the new project's
license. `--project-license unset` removes the project-level license metadata
and preserves the boilerplate license as `THIRD_PARTY_NOTICES.md`; the project
owner must then select its own license according to applicable policy.

The command customizes project files, regenerates `uv.lock`, and removes its
one-time templates and tests. It never commits, rewrites history, changes a
remote, or pushes.

## Recreate the Project Environment

If the initial environment is active, deactivate it. Then replace it so its
shell prompt uses the new distribution name and synchronize the dependencies:

```bash
deactivate
uv venv --clear --prompt "example-service"
uv sync --locked
```

Omit `deactivate` when no virtual environment is active. `--clear` replaces
the existing `.venv`; do not use it for an environment containing unrecorded
manual changes.

## Configure Git Identity and Signing

Set repository-local identity when it should differ from the global Git
configuration:

```bash
git config --local user.name "Your Name"
git config --local user.email "you@example.com"
```

For GPG signing, list available secret keys, copy the long key ID from the
`sec` entry, and configure signing for this repository:

```bash
gpg --list-secret-keys --keyid-format=long
git config --local user.signingkey YOUR_KEY_ID
git config --local commit.gpgsign true
git config --local tag.gpgsign true
```

Verify the effective local configuration without exposing private key
material:

```bash
git config --local --list
```

## Complete Setup and Verify

After setup:

1. complete `docs/project/definition.md`;
2. decide only technical questions required for the first useful milestone;
3. apply the selected host's documented remote settings;
4. add only required CI secrets and integrations;
5. install local hooks; and
6. run the complete verification.

```bash
git remote -v
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
uv lock --check
uv run pre-commit run --all-files
uv run pre-commit run --all-files --hook-stage pre-push
uv build
```

For the meaning and constraints of individual setup fields, consult the
[customization reference](project/customization.md).
