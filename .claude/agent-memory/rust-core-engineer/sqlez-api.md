---
name: sqlez-api
description: Verified sqlez/db API signatures used for zenith_local_history store (fork sha 8bcf87ad77 + feat/local-history)
metadata:
  type: reference
---

- `Connection::open_file(&str) -> Connection` (falls back to shared in-memory on failure), `open_memory(Option<&str>)` named shared-cache: crates/sqlez/src/connection.rs:65,69. Connection is `Send`, not `Sync`.
- `connection.migrate(NAME, MIGRATIONS, &mut Domain::should_allow_migration_change)`: crates/sqlez/src/migrations.rs:37; `Domain` trait (NAME, MIGRATIONS consts): domain.rs:3. Multi-statement migration strings OK; STRICT tables work.
- `exec/exec_bound::<B>/select/select_bound::<B,C>/select_row/select_row_bound` return a closure to call: `conn.exec_bound::<(&str,i64)>(sql)?((a,b))?`. crates/sqlez/src/typed_statements.rs. Tuples Bind/Column up to ~9; `Option<T>`, `Vec<u8>`, `&str`, `i64` ok. `with_savepoint(name, || Result)`: savepoint.rs:10.
- No `changes()` helper in sqlez; use `select_row::<i64>("SELECT last_insert_rowid()")`.
- `zed_env_vars::ZED_STATELESS` (LazyLock<bool>) for memory fallback. `zstd::encode_all/decode_all`, level 3 as agent/db.rs. sha2 `format!("{:x}", Sha256::digest(b))`.
- Fork CLAUDE.md is `AGENTS.md`. No `zenith_core` crate exists yet (2026-11-20).
