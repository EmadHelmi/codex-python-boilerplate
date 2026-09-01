# DB Miniature

DB Miniature is a standalone Python tool for building a statistically and
relationally production-shaped miniature of a MySQL database. The resulting
database is intended for safe, local database-engineering experiments where a
full production clone is impractical.

The project focuses on preserving useful data characteristics rather than
copying the same percentage of rows from every table. Those characteristics
include schema, distributions, cardinality, temporal shape, relationship
fan-out, aggregate integrity, rare cases, and representative row sizes.

## Project Status

The repository currently contains the project and engineering foundation.
Database inspection, profiling, planning, extraction, loading, and validation
commands have not been implemented yet.

The first implementation milestone will establish safe structural inspection
and bounded, read-only profiling for MySQL.

## Design Priorities

- Treat the production database as read-only.
- Prefer conservative, observable, and interruptible queries.
- Never use naive per-table random sampling or `ORDER BY RAND()`.
- Preserve dependency closure and business aggregate integrity.
- Keep sampling deterministic and configuration human-reviewable.
- Make incomplete, skipped, and approximate profile results explicit.
- Keep credentials and sensitive configuration outside version control.
- Remain standalone from Django unless a later integration justifies an
  adapter.

## Development

The project requires Python 3.14 and uses
[`uv`](https://docs.astral.sh/uv/) for dependency and environment management.

Create or synchronize the development environment:

```bash
uv sync
```

Run the current quality checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run lint-imports
```

Repository documentation and agent configuration are described in the
[repository agent configuration](docs/project/agent-configuration.md).
