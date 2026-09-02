# GitLab Repository Settings

Repository files define the reusable automation baseline. Apply and verify
these settings separately after creating the GitLab project because local
files cannot enforce remote permissions or protected-branch policy.

## General

- Use `main` as the default branch.
- Enable issues when the project uses GitLab for work tracking.
- Use squash merging and automatically delete merged source branches.
- Disable unused project features.

## Merge Requests and Protected Branches

- Protect `main` from deletion and force-pushes.
- Require merge requests for ordinary changes.
- Require successful pipelines and resolved discussions before merge.
- For collaborative projects, require at least one approval and Code Owner
  approval when the GitLab tier supports it.
- Keep emergency administrator bypass narrow and auditable.

Required pipeline jobs are:

- `quality`;
- `validate-metadata` for merge requests.

## CI/CD and Security

- Protect and mask sensitive CI/CD variables.
- Review runner trust boundaries before exposing protected variables.
- Enable dependency, secret, and static-analysis features supported by the
  deployed GitLab edition and organization policy.
- Configure dependency-update automation explicitly; this boilerplate does
  not assume an external Renovate or Dependabot service.

## Verification

1. Open a test merge request.
2. Confirm both required jobs run and pass.
3. Confirm an ordinary contributor cannot push directly to `main`.
4. Confirm approval and Code Owner requirements match project policy.
5. Confirm security reports use a private channel.
