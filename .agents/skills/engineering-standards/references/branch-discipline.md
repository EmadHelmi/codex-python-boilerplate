<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Optional Strict Branch Discipline

Classification: **BOILERPLATE / REUSABLE PROJECT BASELINE**.

Application: **OPT-IN**. Apply only when a repository explicitly adopts strict issue-numbered branches. This is not a
public contribution policy merely because it is available.

Git state changes remain subject to [`AGENTS.md`](../../../../AGENTS.md). Implementation approval does not authorize
branch creation, staging, committing, merging, rebasing, or other Git mutations.

## Branch Scope

- Every meaningful change MUST belong to an appropriately scoped branch.
- A branch MUST represent one coherent issue, feature, fix, improvement, documentation change, or independently
  reviewable unit of work.
- Do not accumulate unrelated work because a branch is already checked out or treat a working-tree change as belonging
  to the current branch merely because it is present.
- Before staging or committing, verify that each change belongs to the branch purpose.
- Keep out-of-scope discoveries separate and handle them through an appropriate branch or separately approved workflow.
- Do not bundle unrelated cleanup, refactoring, formatting, documentation, or fixes unless required by the intended
  change.
- Preserve unrelated pre-existing working-tree changes. Do not stage, modify, revert, or commit them for this branch.

## Commit Scope

- Commits MUST contain only changes relevant to the branch purpose.
- Inspect the staged diff and exclude unrelated files or hunks before committing.
- Prefer coherent commits that represent understandable steps within the branch purpose.
- Do not use broad staging such as `git add .` when it could include unrelated changes without first verifying exactly
  what will be staged.
- Never use a commit as a container for unrelated outstanding work.
- If a file mixes relevant and unrelated changes, stage only relevant hunks when safe.

## Branch Naming

Use:

```text
<type>/<number>-<short-name>
```

The numeric component is mandatory under this profile. It MUST NOT be omitted, replaced by a non-numeric identifier,
or treated as optional.

Allowed types:

- `feat` — new functionality or behavior;
- `bugfix` — ordinary bug fix;
- `hotfix` — urgent production fix requiring expedited handling;
- `imp` — improvement to existing behavior or implementation;
- `refactor` — structural change without intended behavioral change;
- `perf` — performance improvement;
- `test` — test-only work;
- `docs` — documentation-only work;
- `build` — dependency, packaging, or build-system work;
- `ci` — CI/CD or pipeline work;
- `chore` — maintenance not covered by a more specific type.

### Numbering

- Use the available issue or task number. Never replace a known one with a locally generated sequence number.
- If no issue or task number is available, allocate a mandatory incremental fallback number independently per type.
- Start a type's fallback sequence at `1`. Each later candidate is one greater than the highest fallback previously
  allocated for that type.
- If a candidate is already used by any branch of the same type, including an issue-based branch, advance to the first
  higher unused number. Do not intentionally skip an available candidate.
- Never reuse a fallback number for the same type, even after the earlier branch is merged, renamed, closed, or deleted.
- The same fallback number MAY be used under different branch types.
- Before allocating, inspect relevant local and remote refs, branch history, or the established registry to determine
  both prior fallbacks and all numeric components used for that type.
- Do not guess. If neither an issue/task number nor a reliable fallback can be established, stop and surface the
  uncertainty.
- Never present a fallback number as an issue or task identifier.

Names MUST use an allowed type, the correct mandatory number, and a short descriptive lowercase kebab-case name. Avoid
spaces, underscores, uppercase characters, and unnecessary wording.

Unless a stricter policy applies, names SHOULD match:

```regex
^(feat|bugfix|hotfix|imp|refactor|perf|test|docs|build|ci|chore)/[1-9][0-9]*-[a-z0-9]+(?:-[a-z0-9]+)*$
```

Examples:

```text
feat/123-add-market-order
bugfix/456-fix-fee-calculation
hotfix/789-restore-withdrawals
imp/321-improve-order-validation
refactor/852-split-payment-service
perf/741-reduce-order-query-count
test/963-cover-settlement-flow
docs/654-update-api-guide
build/151-update-ruff
ci/160-add-security-check
chore/171-clean-dev-scripts
feat/1-add-market-order
feat/2-add-stop-limit
bugfix/1-fix-fee-calculation
bugfix/2-fix-balance-rounding
```

## Existing Policy

- Explicit repository or organization Git policy takes precedence.
- Public contributors follow the repository's contribution policy and are not subject to this optional profile unless
  that policy adopts it.
- Follow existing branch types, naming, issue requirements, and protection rules instead of introducing a competitor.
- A more specific compatible policy may narrow this profile.
- Surface a material conflict instead of overriding repository policy silently.
