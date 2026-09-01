<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Architecture Core Standards

Classification: **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL**.

Application: Read when creating or changing Python source or test files.

These standards are intentionally anti-ceremony. They do not require Clean Architecture, DDD layers, ports,
repositories, factories, services, or CQRS for simple code. Introduce structure only for an actual boundary, policy,
business concept, or source of complexity.

## Python Design

- Prefer the simplest design that cleanly expresses the current requirement. Do not introduce interfaces, factories,
  strategies, DTO layers, or indirection for hypothetical future use.
- Prefer composition over inheritance unless there is a genuine subtype relationship or framework requirement.
- Use `Protocol` for behavioral contracts and dependency inversion when structural typing is sufficient. A meaningful
  architectural boundary can justify a protocol even before multiple implementations exist.
- Use `abc.ABC` when nominal inheritance, shared behavior, or runtime abstract-method enforcement is useful. Do not
  define both a `Protocol` and an ABC for the same contract unless they serve distinct purposes.
- Mark intentional overrides with `@override` when supported by the project's Python compatibility policy.
- Use `@property` for cheap, side-effect-free attribute-like access. Use a method for I/O, state changes, expensive
  work, or behavior that can fail in non-trivial ways.
- Prefer module-level functions when behavior does not naturally belong to instance or class state. Use `@staticmethod`
  only when the operation genuinely belongs in the class namespace without class state, and use `@classmethod` for
  class-level behavior or meaningful alternative constructors.
- Avoid metaclasses, `__del__`, bytecode manipulation, and similar advanced runtime machinery unless a concrete
  requirement makes the complexity worthwhile.
- Keep dependencies directional and avoid circular imports. Use `TYPE_CHECKING` when it is the cleanest typing boundary,
  but not to conceal an avoidable architectural cycle.
- Treat package re-exports as an explicit public-API decision. Do not ban or add `__init__.py` re-exports by default.
- Keep abstractions cohesive: a boundary should own a real concept, policy, or invariant instead of merely forwarding
  calls unchanged.

## Architecture Scope and Dependency Direction

- Do not introduce architectural layers, ports, repositories, services, or domain abstractions merely to conform to
  Clean Architecture or DDD. Add them only when they represent a real business concept, dependency boundary, or source
  of complexity.
- When explicit layers or ports exist, keep dependencies pointing toward the code that owns domain policy. Domain code
  must not depend on presentation, persistence, transport, framework, or infrastructure details. Application code may
  depend on the domain and inward-owned ports, while infrastructure implements those ports.
- When a dedicated domain layer exists, keep it framework-agnostic. Do not import ORM models, HTTP objects, serializers,
  task frameworks, or infrastructure clients into it. Do not create a separate domain layer for simple CRUD code when
  it would only duplicate framework models.
- Keep delivery mechanisms such as HTTP views, CLI commands, message consumers, and task entry points focused on
  delivery concerns. When separate application or domain behavior exists, translate external input, invoke that
  behavior, and translate the result back. Keep business policy out, but do not add a service layer merely to make a
  simple handler thinner.
- Keep application services and use cases focused on orchestration: load required state, invoke domain behavior,
  coordinate ports, define transaction boundaries, and return an application result. Do not move domain rules into
  application services merely to keep domain objects small.
- Keep persistence, external APIs, queues, caches, filesystems, and framework integrations in infrastructure adapters.
  Infrastructure may depend on inner-layer contracts; inner layers must not depend on concrete infrastructure
  implementations.
- Define a port or interface in the innermost layer that requires the capability, not beside the outer implementation
  that happens to provide it.
- Treat dependency direction as an architectural constraint, not merely a framework boundary. Internal packages should
  depend according to ownership and policy direction, not convenience.
