# 12 — Database Tool

## Goal

DataGrip-lite inside Zed: connect, browse schema, run SQL with completion, view/edit results in a grid, export.

## Parity checklist

| Feature | v1 | later |
|---|---|---|
| Connections: MySQL/MariaDB, PostgreSQL, SQLite | ✅ | |
| SQL Server, Redis, MongoDB | | ✅ |
| SSH tunnel, SSL options | ✅ | |
| Read creds from project `.env` (Laravel/WP `wp-config.php`) | ✅ | |
| Schema tree: dbs → schemas → tables/views → columns/indexes/FKs | ✅ | |
| SQL console per connection, run statement at cursor / selection | ✅ | |
| Schema-aware SQL completion | ✅ (via LS) | |
| Results grid: virtualized, sort, filter, copy | ✅ | |
| Edit cells, add/delete rows, submit as transaction | ✅ | |
| Table data editor (open table) | ✅ | |
| Export CSV/JSON/SQL inserts | ✅ | |
| Import CSV | | ✅ |
| Query history | ✅ | |
| Explain plan view | | ✅ |
| ER diagram | | ✅ |
| Schema diff / migrations | | ✅ |
| Agent access: expose DB via MCP to agents (read-only default) | ✅ (via 06) | |

## UX

- Right dock "Database" panel: connection tree, toolbar (+, refresh, console, disconnect).
- Console = `.sql` buffer bound to a connection (status bar shows connection/schema picker); `cmd-enter` runs statement at cursor.
- Results = bottom/center `Item` with tabs per result set; grid component with editable cells, pending-changes highlight, Submit/Revert.
- Production safety: connection flag `read_only` and `confirm_writes` (prompt before UPDATE/DELETE without WHERE, DDL).

## Architecture

- Crate `zenith_db` (+ `zenith_grid` UI component — reusable, also for CSV viewing).
- Drivers: `sqlx` (MySQL, Postgres, SQLite) async on background executor; one pool per connection; cancellation support.
- Introspection: `information_schema` / `pg_catalog` / `sqlite_master` queries → cached schema model; refresh on demand + after DDL.
- SQL completion: run a SQL language server (`sqls` or `postgres-language-server`) configured with the active connection, *or* our own completion provider from cached schema (decide after spike).
- Statement splitting: tree-sitter SQL or `sqlparser` crate.
- Grid: GPUI `uniform_list` virtualization, column widths, cell editor overlay; pagination with `LIMIT/OFFSET` + "fetch more".
- Edits: track row identity by primary key; generate parameterized UPDATE/INSERT/DELETE; run in a transaction.
- Secrets: passwords in macOS Keychain (`keyring` crate *or* Zed's credentials provider — *verify*); never in settings JSON.
- SSH tunnel: `russh` or spawn `ssh -L` (start with spawning `ssh`).

## Settings

```json
"zenith": {
  "database": {
    "enabled": true,
    "page_size": 500,
    "confirm_writes": true,
    "connections_file": ".zed/databases.json"
  }
}
```
`databases.json` holds host/port/user/db/ssh — no passwords.

## Security

- Parameterized queries for all generated SQL.
- Keychain-only secrets; `.zed/databases.json` safe to commit.
- MCP exposure read-only unless connection flag `agent_write: true`.

## Milestones

1. Spike: sqlx connect + introspection + simple results table (2 wk).
2. Connection manager + Keychain + `.env` import (1 wk).
3. Schema tree panel (1 wk).
4. Console + run at cursor + results grid read-only (2 wk).
5. Grid editing + transactions (2 wk).
6. SQL completion (1–2 wk).
7. Export, history, SSH tunnel (1–2 wk).
8. MCP read-only tools (1 wk).

## Tests

- Docker-based integration tests (mysql, postgres) gated behind a feature flag/CI job.
- SQLite tests in default suite.
- Edit → SQL generation unit tests (quoting, NULLs, types).

## Risks

- Largest feature; grid UX performance on GPUI — prototype grid early (milestone 1).
- Type mapping breadth (JSON, geometry, binary) — show raw for unsupported.
- Binary size/compile time increase from sqlx — measure.

## Effort

2–3 months.
