<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Personal Python Test Conventions

Classification: **PERSONAL CONVENTION**.

Application: Read when creating or changing Python tests. Apply these DAMP-oriented preferences when compatible;
explicit framework, repository, organization, and project requirements take precedence.

## Structure and Naming

- Favor DAMP tests over aggressive DRY abstractions. Keep each test understandable in isolation, even when that
  requires small amounts of intentional duplication.
- In pytest-native code, prefer standalone test functions by default.
- Introduce a test class only when grouping tests around the same behavior or unit materially improves navigation or
  shared context.
- Framework-specific testing conventions may deliberately prefer another structure.
- Name pytest-native test classes `Test<UnitOrBehavior>`. For `unittest.TestCase`-based tests, follow the repository's
  existing class naming convention.
- Name tests after observable behavior and scenario rather than private implementation details. Prefer names such as
  `test_<behavior>_when_<condition>` or `test_<operation>_<expected_outcome>` when they read naturally.
- Prefer `test_<subject>.py` for new pytest test modules. Preserve an established repository naming convention instead
  of renaming files solely for style.
- Organize tests so their relationship to the production capability is easy to locate. Mirror production package
  structure when it improves navigation, but do not create directory hierarchies solely for symmetry.
- Keep Given, When, and Then visually obvious from the test body, normally using blank lines between meaningful
  phases. Add phase comments only when the structure is not already clear.
- Use test comments to explain non-obvious business rationale, historical regressions, or surprising setup constraints
  instead of narrating obvious code.

## Assertions and Expected Values

- Prefer explicit expected values that are independent of the production calculation. Hardcode expected literals or
  domain values when practical instead of recomputing the expected result with the same algorithm as the code under
  test.
- Keep behavioral assertions inline. Do not hide expected outcomes behind shared `validate_*()` or `assert_*()`
  helpers. Use specialized assertion helpers only when they materially improve diagnostics for a genuinely reusable
  technical contract.

## Test Data and Setup

- Use test helpers primarily to construct inputs and establish preconditions. Keep the action under test and its
  important outcomes visible in the test body.
- Require behavior-relevant test-data values explicitly at the call site. Construction-helper defaults may hide
  incidental boilerplate but must not hide values that determine the scenario or expected outcome.
- Prefer direct object construction for simple test data. Introduce small `make_*` or `build_*` helpers when repeated
  construction becomes noisy; do not introduce elaborate test-data builder frameworks for simple objects.
- Use fixtures for reusable context or resources whose lifecycle matters. Prefer ordinary helper functions for simple
  data construction when fixture injection would obscure the scenario.
- In pytest-native tests, prefer explicit fixtures or local setup over `setUp()` and `tearDown()`. Use `setUp()` and
  `tearDown()` when working within an existing `unittest.TestCase` style and the lifecycle is genuinely shared by the
  class.
- Use pytest test classes for logical grouping, not for sharing mutable state between tests. Each test must remain
  independently executable.

## Multiple Scenarios

- Keep ordinary test bodies free from control flow that creates multiple hidden scenarios. Use parameterization or
  subtests for genuinely table-driven cases with explicit inputs and expected outcomes.
- Prefer separate tests over parameterization when cases require substantially different setup, explanations,
  assertions, or business meaning. Do not compress scenarios merely to reduce line count.
- Give parameterized cases meaningful IDs when raw parameter representations do not make the scenario obvious in test
  output.

## Execution

- Do not add a `__main__` execution guard to ordinary test modules.
