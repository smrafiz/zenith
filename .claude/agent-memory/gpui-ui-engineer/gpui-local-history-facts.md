---
name: gpui-local-history-facts
description: Verified fork facts for zenith_local_history C3 (history Item embedding FileDiffView, Store read path, ProjectPanel focus target); fork 9e6de83562 + uncommitted
metadata:
  type: reference
---

- `FileDiffView::new(old, new, Entity<BufferDiff>, project, Entity<Workspace>, window, cx)` is pub, `build_buffer_diff(&old,&new,&mut AsyncApp)` is pub (`git_ui_core/src/file_diff_view.rs:105,223`); its `editor`/`old_buffer` fields are private. Re-diff is a 250 ms debounce (`RECALCULATE_DIFF_DEBOUNCE`, private): tests `advance_clock(300ms)` + `run_until_parked`. An old buffer with no file shows breadcrumb "untitled <-> a.txt".
- `AsyncWindowContext` derefs to `AsyncApp`; its `AppContext::new` returns `Entity<T>` directly (not Result), so `cx.new(..)` works inside `cx.spawn_in`.
- Embedded editors: the Item's `focus_handle` = list handle; list div gets `key_context` + `menu::Select*/Confirm/Cancel` listeners only (editor Escape must not reach `menu::Cancel`). Same action key (`alt-shift-h`) on an open tab = activate + refocus list (dedupe via `workspace.items_of_type::<T>`), no extra keymap needed.
- Project-panel context-menu actions dispatch with the panel focused: pick `ProjectPanel::selected_entry_project_path` only if `panel.focus_handle(cx).contains_focused(window, cx)` and the entry is a file, else `workspace.active_item(cx)?.project_path(cx)`; override `Item::active_project_path` on the new item.
- Store reads: `Store` is not Sync; reads go through the capture owner task as `Job::List/Content` with a `oneshot` reply, answered in queue order. Open the buffer FIRST (opening records the "open" baseline), then send the list job, or the baseline is missing.
- Tests: `KeymapFile::load_panic_on_failure(json, cx)` rejects unknown action names (verifies zed_actions registration). Needs dev-deps `remote_connection` test-support (else E0004 Mock) and `fs`/`editor`/`workspace`/`project` test-support. `RelPath::from_unix_str("a.txt")?.into()` makes an `Arc<RelPath>`.
- Child test module trick: `#[cfg(test)] #[path = "history_view_tests.rs"] mod tests;` inside history_view.rs gives tests access to private fields; test names then contain `history_view`.
- Disk: a `cargo test -p zenith_local_history` build dropped free space 33 -> 28 GiB (30 GiB gate blocks reruns).
