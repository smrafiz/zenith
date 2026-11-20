# 05 — Local History

## Goal

Automatic, git-independent history of every file change, browsable and restorable — like JetBrains Local History.

## Parity checklist

- [ ] Snapshot on save (must)
- [ ] Snapshot on external change (git checkout, formatter, agent edit) (must — critical for agentic work)
- [ ] Labels: auto events ("Before agent edit", "Git checkout", "Reformat") (must)
- [ ] Show History for file: list of revisions + diff vs current (must)
- [ ] Revert file (must); revert selected hunk (milestone 2)
- [ ] "Opened" baseline snapshot when a file is first opened (must)
- [ ] Show History for folder/project (later)
- [ ] Put Label manually (later)
- [ ] Recover deleted files (must)
- [ ] Retention (days / size cap) (must)

## UX

- Command palette + `alt-shift-h`; project panel context menu gets "Local History…". Editor right-click menu deferred.
- History opens a center `Item`: left list of revisions (time, label, size Δ), right diff view (reuse Zed's diff/editor infrastructure, read-only base).
- Buttons: Revert, Copy content; Revert Hunk in milestone 2.
- Deleted files: "Recover Deleted Files" action listing paths that have snapshots but no file.

## Architecture

- Crate: own `zenith_local_history` with its own `store.rs`; no `zenith_core` yet (plan 15: store extracted on second use). Upstream hooks (4/5): `Cargo.toml` members, workspace dep, `zed_actions` module, project_panel menu line.
- Storage: SQLite (via `db`/`sqlez`) in `paths::data_dir()/local_history/history.db` (macOS `~/Library/Application Support/Zenith/`), a separate file, NOT the shared `db.sqlite` (pattern: `crates/agent/src/db.rs`):
  - `blobs(hash TEXT PK, content BLOB zstd-compressed)` — content-addressed dedupe
  - `revisions(id, worktree_root, rel_path, blob_hash, ts, label, source)`
- Hooks (verified, fork @ 8bcf87ad77):
  - Save: `BufferEvent::Saved` `language/src/buffer.rs:337`, subscribed via `BufferStoreEvent::BufferAdded` `project/src/buffer_store.rs:92`. Reload: `BufferEvent::Reloaded` `buffer.rs:341`.
  - External changes: `project::Event::WorktreeUpdatedEntries` `project.rs:384` (debounced 500 ms). React to Updated/AddedOrUpdated, never Loaded (= initial scan).
  - Diff and revert: reuse `git_ui_core::file_diff_view::FileDiffView` (`file_diff_view.rs:105`) + `RestoreDiffOperations` (`buffer_diff.rs:53`) for Revert Hunk.
  - Agent panel edits: label "Before agent edit" (find hook point in `agent` crate; *verify*). Unverified: whether agent `edit_file` triggers `Saved`.
- Ignore rules: skip private files (`File::is_private` `buffer.rs:401`) and ignored entries (`Entry::is_ignored` `worktree.rs:4013`); respect `file_scan_exclusions`; default exclusions `wp-config.php`, `.env*`; size limit (default 2 MB), binary detection.
- Retention: background task daily — delete revisions older than N days, then orphan blobs.
- Remote projects: snapshot on the client side using buffer content (works over SSH without server changes).

## Data & settings

```json
"zenith": {
  "local_history": {
    "enabled": true,
    "retention_days": 14,
    "max_file_size_kb": 2048,
    "max_db_size_mb": 1024,
    "snapshot_external_changes": true
  }
}
```

## Actions & keymap

`ShowFileHistory`, `ShowProjectHistory`, `PutLabel`, `RecoverDeletedFiles`. JetBrains has no default key; add `alt-shift-h` (configurable).

## Milestones

1. Storage + snapshot on save (+ "Opened" baseline) + retention.
2. History view (list + diff) + revert file + Revert Hunk.
3. External-change snapshots + deleted-file recovery.
4. Agent-edit labels.
5. Labels, project history.

## Chunks

| Chunk | Scope | Owner |
|---|---|---|
| C1 | Storage (`store.rs`, blobs, revisions, retention) | rust-core-engineer |
| C2 | Snapshot on save (+ Opened baseline, ignore rules) | rust-core-engineer |
| C3 | History `Item` (list + diff) | gpui-ui-engineer |
| C4 | Revert file / hunk | gpui-ui-engineer |
| C5 | External change + recover deleted | rust-core-engineer / gpui-ui-engineer |

## Tests

- Dedupe: same content twice → one blob.
- Retention removes old rows and orphan blobs.
- gpui test: edit+save 3× → 3 revisions; revert restores content.
- Ignore rules honoured.

## Risks

- Write amplification on big repos during `git checkout` — debounce + batch insert + size caps.
- DB growth — enforce `max_db_size_mb` with oldest-first eviction.

## Effort

1–2 weeks.
