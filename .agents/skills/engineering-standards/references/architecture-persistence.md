<!-- Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi) -->

# Persistence Boundary Standards

Classification: **GENERAL / ECOSYSTEM / PROJECT-NEUTRAL**.

Application: Read when creating or changing repositories, ORM or persistence adapters, aggregate loading or saving,
query services, missing-object semantics, Unit of Work, transaction ownership, or persistence mapping.

## Repositories

- Use a repository to abstract persistence of an aggregate root when persistence is a meaningful architectural
  boundary. Do not introduce repositories merely to wrap ORM calls.
- Define repositories around aggregate roots, not database tables or every persisted entity.
- Do not introduce a generic CRUD repository by default. Prefer small repositories whose operations reflect aggregate
  and application needs.
- Do not leak ORM query objects, persistence models, sessions, managers, or query-building APIs through repository
  contracts. Interfaces should speak in domain or application types and concepts.
- When a dedicated domain model exists, repositories should load and persist domain aggregates rather than expose
  persistence models.
- Make missing-object semantics explicit. Use nullable results or domain/application-specific not-found errors
  consistently instead of leaking persistence exceptions.
- Persist aggregate changes through aggregate-oriented operations such as `save()`; avoid arbitrary field-level update
  APIs that bypass domain behavior.
- Keep reporting, analytics, projections, and other read-optimized queries out of aggregate repositories when they do
  not load aggregates for domain behavior. Use dedicated query or read services.
- Add domain-specific repository queries only for stable application needs; do not turn repositories into collections
  of one-off query permutations.
- Do not let repositories define business transaction boundaries. Transaction scope belongs to the application use
  case or Unit of Work coordinating the operation.
- Introduce a Unit of Work only when explicit repository coordination or transaction lifecycle provides real value;
  do not add one solely to conform to an architectural pattern.
- Keep repository implementations focused on persistence and mapping. Business decisions and invariants belong to
  domain or application behavior.
