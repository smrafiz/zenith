---
name: gpui-capture-apis
description: Verified Zed APIs for buffer-save capture in fork (zenith_local_history C2), fork sha 5601c64bff
metadata:
  type: reference
---

Verified @ 5601c64bff (feat/local-history), cargo check -p zenith_local_history passed:
- `cx.observe_new(|project: &mut Project, _, cx: &mut Context<Project>| ..)` works for per-project hooks; `project.is_local()` takes no cx (project.rs:3163), `project.buffer_store()`.
- `BufferStoreEvent::BufferAdded(Entity<Buffer>)` buffer_store.rs:92; `BufferEvent::Saved` buffer.rs:337.
- `worktree::File::from_dyn(buffer.file())`; pub fields worktree, path, disk_state, entry_id, is_local, is_private (worktree.rs:3838). `Worktree::entry_for_id` :2951; `Entry.is_ignored`.
- `WorktreeSettings::get(Some(SettingsLocation{worktree_id, path}), cx).is_path_excluded(&RelPath)` (worktree_settings.rs:31).
- `RelPath::as_unix_str()` crates/path/src/rel_path.rs:268; `buffer.as_rope()` (text.rs:2072) derefs through Buffer.
- `AsyncApp::update(|cx| ..)` returns R (no Result).
- Agent edit_file saves: agent/src/tools/edit_session.rs:186 ensure_buffer_saved -> project.save_buffer (:208), so Saved fires.
- Test setup: SettingsStore::test(cx) loads default.json merged with test overrides; update_user_settings replaces whole user content.
- BSD sed -i needs '' on macOS; use python for edits.
- (@5601c64bff, C2 fixes) `Buffer::saved_version()` buffer.rs:1451 + `rope_for_version(&clock::Global)` text.rs:2076 (via Deref) = text as saved; `Entry.canonical_path.is_some()` marks every symlink, `is_external` outside root (worktree.rs:4008-4032); single-file worktree has empty `File.path`, real name = `worktree.abs_path().file_name()`; `RelPath::from_unix_str(&OsStr)` -> Result<&RelPath>; `project::*` re-exports `fs::Fs` (create_symlink); FakeFs cannot save through a symlink ("not a file"). Start save, then edit, then await = edit lands mid-save in gpui tests.
