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
- Storage: SQLite (via `db`/`sqlez`) in `paths::data_dir()/local_history/history.db` (macOS `~/Library/Application Support/Zenith/local_history/`, not `~/.local/share/zenith`), a separate file, NOT the shared `db.sqlite` (pattern: `crates/agent/src/db.rs`):
  - `blobs(hash TEXT PK, content BLOB zstd-compressed)` — content-addressed dedupe
  - `revisions(id, worktree_root, rel_path, blob_hash, ts, label, source)`
- Hooks (verified, fork @ 8bcf87ad77):
  - Save: `BufferEvent::Saved` `language/src/buffer.rs:337`, subscribed via `BufferStoreEvent::BufferAdded` `project/src/buffer_store.rs:92`. Reload: `BufferEvent::Reloaded` `buffer.rs:341`.
  - External changes: `project::Event::WorktreeUpdatedEntries` `project.rs:384` (`FS_WATCH_LATENCY` 100 ms, `worktree.rs:84`; not debounced). React to Updated/AddedOrUpdated, never Loaded (= initial scan).
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
    "max_db_size_mb": 500,
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

## Progress

Fork branch `feat/local-history` (C1–C5 done in fork, unpushed unless pushed later; `cargo check -p zenith` app check and running-app check pending): `55334a5615`, `5601c64bff`, `ec20e7e720`, `9e6de83562`, `14d1989fc9`, `f130b256d0`, `3e4a047e1b`, `685a9e1c13` (C3); `58d3a3ee58`, `0aaf01fa8c` (C4); `aa2f7b59de`, `511c689f8e` (C5).

| Chunk | State | Notes |
|---|---|---|
| C1 storage | done in fork | `zenith_local_history/src/store.rs`: dedupe, retention, DB dir 0700, `history.db` 0600. Default `max_db_size_mb` 500 (0 is raised to 1). |
| C2 capture | done in fork | Snapshot on open and save through one gate (`capture.rs` `is_trackable`): local files only (`file.is_local`), skips private, ignored, external and symlinked entries (a symlinked plugin dir gets no history, deliberate), `file_scan_exclusions`. `wp-config.php` and `.env*` are never stored (`store.rs`, also for single-file worktrees). The gate is re-applied when history is shown. |
| C3 view | done in fork | Show History view (revision list + diff), `alt-shift-h`, project panel "Local History…" (6-line hook in `project_panel.rs`, `zed_actions::zenith_local_history`). |
| C4 revert | done in fork | `history_view.rs`: Revert to revision (one undoable diff-applied edit; a "Before revert" snapshot is taken when recording is on) and Copy revision text. Actions `RevertToRevision`, `CopyRevisionText` live in the crate; keys `alt-shift-r` / `alt-shift-c` (`assets/keymaps/zenith.json`). Tab / Shift-Tab use `FocusNextControl` / `FocusPreviousControl`; status line. Revert Hunk not done. |
| C5 external changes + recover | done in fork | `capture.rs`: external-change capture on `WorktreeUpdatedEntries`, only for files that already have history, same gate, 2 s settle for dirty buffers (re-gated after), refuses symlink / non-regular / oversize / non-canonical paths, bounded read. `recover.rs`: Recover Deleted Files picker (command palette only, no key). Restore safeguards: strict `RelPath`, root equality, secret / private / excluded refusal, no symlinks, never overwrites, local and trusted projects only, `create_file` (O_EXCL) then `atomic_write`; restored file mode is 0600. Deleted list capped at 20000. Setting `snapshot_external_changes` (default true). |

Known limits (C3–C5):

- Recover picker has no list role or input label (upstream picker untouched).
- Accessibility tree not covered by tests; needs a VoiceOver pass.
- History is keyed only by absolute root path: a different repo cloned to the same path is offered the old files. Needs project identity (future work).
- A save within 2 s of an external change to a dirty file loses the disk text.
- The restore race is not testable on `FakeFs`.
- A deleted file ignored by name can be restored and then ignored.
- Files never opened or saved get no external revision.
- Symlinked or external files get no history.

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
