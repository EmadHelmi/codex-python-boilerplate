# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for decisions
whose reasoning should remain available to future contributors.

## Purpose

An ADR records a meaningful decision, the context in which it was made, the
alternatives that were considered, and the consequences the project accepts.
ADRs preserve decision history; they do not replace project requirements,
engineering standards, or implementation plans.

## When to Write an ADR

Record a decision when it materially affects one or more of the following:

- architecture or important boundaries;
- security or sensitive-data handling;
- persistent data;
- public interfaces or external contracts;
- important dependencies or infrastructure;
- deployment or operational behavior;
- testing strategy;
- developer workflow or long-term maintainability.

Do not create ADRs for local, reversible implementation details whose
rationale would not be useful after the current change.

## Statuses

Each ADR has exactly one of these statuses:

- `Proposed`: under consideration and not authoritative;
- `Accepted`: approved and currently authoritative;
- `Rejected`: considered but not selected;
- `Superseded`: replaced by a newer accepted ADR.

Only an applicable `Accepted` ADR represents an active project decision.

## Naming and Numbering

ADR filenames use a four-digit, monotonically increasing number followed by a
short kebab-case title:

```text
NNNN-short-decision-title.md
```

Numbers are never reused. A superseding decision receives a new number and
links to the record it replaces.

## Decision Process

1. Confirm that the decision is required by current or immediately upcoming
   work.
2. Check the Decision Register and applicable accepted ADRs.
3. Compare the strongest viable alternatives using project-specific drivers.
4. Obtain the user's explicit acceptance of the decision.
5. Create the ADR from [`template.md`](template.md).
6. Add it to the Decision Register.
7. Plan implementation separately and obtain implementation approval.

Accepting or recording a decision does not authorize its implementation.

## Updating Decisions

Do not rewrite the substance of an accepted ADR to represent a later choice.
When circumstances require a different decision:

1. create a new ADR describing the changed context;
2. mark the previous ADR as `Superseded`;
3. link both records to each other;
4. update the Decision Register.

Minor corrections that do not change the decision or its rationale may be
applied directly.

## Decision Register

| ID | Decision | Status | Date |
| :---: | :--- | :---: | :---: |
| [0001](0001-adopt-codex-native-agent-configuration.md) | Adopt Codex-native agent configuration | Accepted | 2026-08-31 |
