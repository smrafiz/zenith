---
name: gpui-scratches-facts
description: Verified fork facts for zenith_scratches (Fs create/trash/watch, open_abs_path with no project, modal Enter/Escape, error prompt); fork b4130a774e, 2026-11-20
metadata:
  type: reference
---

Verified by reading (compiled with `cargo check -p zenith_scratches --tests`; tests NOT yet run, disk gate blocked):

- `paths::data_dir()` is a plain `PathBuf` (`paths.rs:143`), fine to use against `FakeFs` in tests (no redirect needed).
- `Fs::trash(path, RemoveOptions) -> Result<TrashId>` (`fs/src/fs.rs:129`), FakeFs impl `:3244`. `create_file` with `overwrite:false, ignore_if_exists:false` errors on an existing path (`:3035`). `Fs::watch(path, Duration)` returns `(Stream<Vec<PathEvent>>, Arc<dyn Watcher>)` (`:175`); real watcher needs the dir to exist: `create_dir` first.
- `Workspace::open_abs_path` -> `open_paths` with default `OpenOptions` uses `OpenVisible::None` => invisible worktree (`workspace.rs:4272`), so a file outside any worktree opens without showing a folder in the project panel, and works with a `Project::test(fs, [], cx)` (no worktree).
- Single-line `Editor` inside a hand-rolled modal: Enter/Escape/Up/Down are bound to `menu::*` in the GLOBAL first block of `default-macos.json`; `Editor && mode == full` only owns `enter`. So `.on_action(menu::Confirm / menu::Cancel)` on the modal root is enough. In tests bind `enter`/`escape`/`down` with context `None`.
- Errors from a task: `Task<anyhow::Result<_>>::detach_and_prompt_err(msg, window, cx, |_,_,_| None)` from `workspace::notifications::DetachAndPromptErr`; `window.spawn(cx, async move |cx| ..)` gives an `AsyncWindowContext` for `WeakEntity<Workspace>::update_in`.
- `ListItem::on_secondary_mouse_down(Fn(&MouseDownEvent,&mut Window,&mut App))` exists (`ui/.../list_item.rs:185`) - not a `cx.listener`; capture a `WeakEntity` instead. Context-menu pattern: outline_panel.rs:1781 (`Option<(Entity<ContextMenu>, Point<Pixels>, Subscription)>` + `deferred(anchored())`).
- `ui::utils::reveal_in_file_manager_label(false)` for the Finder label; `App::reveal_path(&Path)` (`gpui/src/app.rs:2162`).
- Left dock hide: `workspace::ToggleLeftDock` (`workspace.rs:482`).
- BSD sed on macOS: `sed -i` needs `''`; use the Edit tool.
- Disk: `target/` was 73G; free space dropped 31 -> 29 GiB during one `cargo check` (30 GiB gate blocks tests).
