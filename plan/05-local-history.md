# 05 — Local History

## Goal

Automatic, git-independent history of every file change, browsable and restorable — like JetBrains Local History.

## Parity checklist

- [ ] Snapshot on save (must)
- [ ] Snapshot on external change (git checkout, formatter, agent edit) (must — critical for agentic work)
- [ ] Labels: auto events ("Before agent edit", "Git checkout", "Reformat") (must)
- [ ] Show History for file: list of revisions + diff vs current (must)
- [ ] Revert file / revert selected hunk (must)
- [ ] Show History for folder/project (later)
- [ ] Put Label manually (later)
- [ ] Recover deleted files (must)
- [ ] Retention (days / size cap) (must)

## UX

- Context menu in editor + project panel: "Local History → Show History", "Put Label".
- History opens a center `Item`: left list of revisions (time, label, size Δ), right diff view (reuse Zed's diff/editor infrastructure, read-only base).
- Buttons: Revert, Revert Hunk, Copy content.
- Deleted files: "Recover Deleted Files" action listing paths that have snapshots but no file.

## Architecture

- Storage: SQLite (via `db`/`sqlez`) in `~/.local/share/zenith/history.db`:
  - `blobs(hash TEXT PK, content BLOB zstd-compressed)` — content-addressed dedupe
  - `revisions(id, worktree_root, rel_path, blob_hash, ts, label, source)`
- Hooks:
  - Buffer saved event from `Project`/`BufferStore` (*verify event name*).
  - Worktree FS change events for external modifications (debounced 500 ms).
  - Agent panel edits: hook before applying agent edits → label "Before agent edit" (find hook point in `agent` crate; *verify*).
- Ignore rules: respect `.gitignore`, `file_scan_exclusions`, size limit (default 2 MB), binary detection.
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

1. Storage + snapshot on save + retention.
2. History view (list + diff) + revert file.
3. External-change snapshots + deleted-file recovery.
4. Agent-edit labels.
5. Hunk revert, labels, project history.

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
