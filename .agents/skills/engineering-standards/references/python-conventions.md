<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Personal Python Conventions

Classification: **PERSONAL CONVENTION**.

Application: Read when creating or changing Python source or test files. Apply these preferences when compatible;
explicit framework, repository, organization, and project requirements take precedence.

## Functions

- Keep functions readable top-to-bottom. Separate meaningful logical blocks with one blank line; add a short comment
  only when intent is not obvious from the code.
- Keep trivial logic inline. Extract a helper when it represents a meaningful operation, materially improves the
  caller, or has genuine reuse; do not extract solely to reduce line count or minor duplication.
- Avoid nested functions by default. Use one when the function is inherently local to its enclosing scope, especially
  for a closure or callback, and extracting it to module scope would expose an implementation detail without improving
  reuse or testability. Keep nested functions small and easy to understand.
- Make parameters required unless the API has a clear, valid default. Do not add defaults merely to make callers more
  convenient. Use `None` as a default only when it is either an intentional API value or an unambiguous sentinel; use
  a dedicated sentinel when "not provided" must be distinguishable from `None`.
- Use keyword-only parameters when they materially improve call-site clarity or prevent ambiguous or unsafe positional
  calls, especially for booleans and configuration-style options. Keep natural, essential operands positional. Do not
  make parameters keyword-only merely for stylistic consistency, and do not change an existing public API to
  keyword-only without considering compatibility.

## Constants

- Declare module-level constants near the start of the module after imports and module metadata.
- Declare class-level constants near the start of the class body before ordinary instance behavior, unless a framework
  or established repository convention requires a different placement.

## Strings

- Prefer f-strings for ordinary interpolation; use an API's native formatting mechanism when appropriate.
- Do not repeatedly concatenate strings in a loop; collect and join fragments or use an appropriate buffer.
- Use `textwrap.dedent()` for multiline strings when source indentation should not be part of the value.

## Imports and Public APIs

- Choose module imports or direct symbol imports based on call-site clarity. Use aliases only to resolve ambiguity or
  meaningfully improve readability.
- Do not re-export symbols from `__init__.py` merely for convenience. Use re-exports only as part of a deliberate
  package-level public API.

## Typing

- Annotate public functions, methods, attributes, and other API boundaries. Add internal annotations when inference is
  unclear or an explicit type materially improves readability or type safety.
- Make optionality explicit whenever `None` is a valid value.
- Avoid `Any` when a more precise type is practical. Use it intentionally at genuinely dynamic or untyped boundaries,
  not as a shortcut around type errors.
- Use `cast()` only when the runtime invariant is known but the type checker cannot prove it; do not use casts to hide
  an incorrect or incomplete type model.
- Prefer fixing dependency direction over introducing `TYPE_CHECKING` imports. Use typing-only imports or postponed
  annotations when they are the cleanest solution rather than a way to hide an architectural cycle.

## Enums

- Use enums for finite value sets owned by the codebase. Do not encode values owned by configuration, the database,
  users, or independently deployed systems as code enums.
- Prefer string-valued enums when values cross APIs, DTOs, logs, persistence, or module boundaries. Use integer values
  only when the integer itself is part of the domain or an existing external contract.
- Keep externally exposed enum values stable unless compatibility or migration is handled explicitly.

## Control Flow

- Use comprehensions for simple transformations and filters. Prefer an explicit loop when the logic has multiple
  stages, side effects, or non-trivial conditions.
- Keep lambdas limited to short, obvious expressions. Prefer a named function when the behavior has meaningful logic
  or deserves a name; use `operator` helpers when they express intent more clearly.
- Use conditional expressions only when the condition and both outcomes remain immediately readable.
- Prefer generators or iterators when values can be consumed lazily and full materialization is unnecessary.

## Object-Oriented Naming

- Name architectural `Protocol` contracts with an `Interface` suffix. Name helper, callback, and typing-only protocols
  after their concrete role rather than forcing the suffix.
- Prefix classes intentionally designed as inheritance bases with `Base`.

## Executable Modules

- Keep import-time behavior side-effect free.
- Put script execution in `main()` and invoke it under `if __name__ == "__main__":`.
