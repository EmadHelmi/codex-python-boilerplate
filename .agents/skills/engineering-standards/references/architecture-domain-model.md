<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Domain Model Standards

Classification: **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL**.

Application: Read when creating or changing entities, value objects, aggregates, aggregate roots, domain invariants,
identity or equality, domain mutation, or cross-aggregate consistency.

## Entities and Value Objects

- Model business concepts explicitly when doing so protects invariants or makes domain behavior clearer. Do not
  introduce entities or value objects merely to wrap primitives without meaningful domain semantics.
- Treat an object as an entity when its identity persists across state changes. Define identity and equality semantics
  from the domain rather than from all current attributes.
- Put behavior that enforces an entity's own invariants on the entity. Prefer intention-revealing domain operations over
  generic setters or arbitrary external mutation.
- Entities may mutate as part of valid domain operations. Encapsulate mutation behind behavior that preserves
  invariants rather than requiring entity-wide immutability.
- Treat an object as a value object when it is defined entirely by its values and has no independent identity.
- Make value objects immutable by default. Operations should return a new value rather than mutate existing state.
- Construct domain objects only in valid states when practical. Validate value-object invariants at creation rather
  than allowing invalid instances to exist temporarily.
- Introduce a value object when it owns meaningful validation, behavior, units, comparison semantics, or domain
  meaning; do not wrap primitives solely for architectural purity.
- Keep entities and value objects focused on domain state and behavior. Do not give them persistence, HTTP, queue,
  filesystem, or other infrastructure responsibilities.

## Aggregates

- Introduce an aggregate only when multiple domain objects must preserve a consistency boundary together. Do not group
  objects merely because they are related or stored near each other.
- Define aggregate boundaries from business consistency rules, not ORM relationships, table structure, or
  object-navigation convenience.
- Expose aggregate mutation through the aggregate root. External code should not mutate internal entities or
  collections directly.
- Keep invariants spanning objects inside an aggregate enforced by its root. Application services should orchestrate
  aggregate operations, not reconstruct aggregate invariants externally.
- Keep aggregates as small as consistency requirements allow. Do not combine objects solely for traversal or
  persistence convenience.
- Reference other aggregates by stable identity rather than embedding their mutable object graph.
- Do not force multi-aggregate invariants into one aggregate merely for immediate consistency. Coordinate separate
  aggregates in the application layer, using domain services or asynchronous consistency when appropriate.
- Prefer one aggregate as a transaction's primary consistency boundary. Modify multiple aggregates atomically only
  when a business invariant genuinely requires immediate consistency.
- Create repositories around aggregate roots, not around every entity or table. Persist internal members through their
  root.
- Do not expose mutable aggregate internals in a way that lets callers bypass invariants. Expose read-only views or
  controlled domain operations.
