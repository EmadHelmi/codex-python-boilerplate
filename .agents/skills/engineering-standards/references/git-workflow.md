<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Git Branch Source Workflow

Classification: **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL**.

Application: Read before creating a branch or deciding how a dependent branch follows its prerequisite.

Git state changes still require the authorization defined by [`AGENTS.md`](../../../../AGENTS.md). These standards do
not authorize branch creation, merge, or rebase operations.

- Create new branches from the repository's primary integration branch, such as `main`, by default.
- Do not branch from the current working branch unless the new work explicitly depends on changes that are not merged.
- When a branch must depend on an unmerged branch:
  - state the dependency explicitly;
  - keep it temporary;
  - after the prerequisite is merged, either rebase the dependent branch onto the integration branch or merge the
    updated integration branch into it, subject to separate authorization.
- Avoid long-lived chains in which one feature branch permanently depends on another.
- Before creating a branch, identify its source and explain any departure from the primary integration branch.
- Never silently choose a non-default source branch.
