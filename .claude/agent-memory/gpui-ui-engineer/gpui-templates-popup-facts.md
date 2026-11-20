---
name: gpui-templates-popup-facts
description: Verified project-panel / worktree / RelPath / Picker facts from zenith_templates (New popup); fork sha b4130a774e + uncommitted
metadata:
  type: project
---

- `ProjectPanel::selected_entry_project_path` is pub (`crates/project_panel/src/project_panel.rs:4497`); `workspace.panel::<ProjectPanel>(cx)` works from a Workspace action (`workspace.rs:5087`). `ProjectPanel::new` is private; tests build it with `ProjectPanel::load(weak_ws, cx.clone())` inside `window.spawn(cx, async move |cx| ..)` (a `VisualTestContext::spawn` gives AsyncApp, wrong type), then `workspace.add_panel`. `select_path_for_test(ProjectPath, &App)` is pub (`:8385`).
- `project_panel::{NewFile, NewDirectory}` are pub actions; the panel only handles them when focused: `workspace.focus_panel::<ProjectPanel>` then `window.dispatch_action`, all in `window.defer` after `hide_modal` (deterministic focus order).
- `util::rel_path::RelPath::new` (`crates/path/src/rel_path.rs:58`) NORMALISES `..` (`a/../x` -> `x`) and only errors when it climbs above the root; it does not reject `..`. Reject `..`/`.`/empty components yourself before calling it. Backslash is only normalised in Windows style.
- `Worktree::create_entry(path, is_dir, content, cx)` (`worktree.rs:964`) does `fs.write`, i.e. OVERWRITES. The snapshot (`entry_for_path`) misses git-ignored unscanned dirs (`vendor/`) and excluded paths, so also check `fs.metadata(abs).await` (local projects only; `Project::fs()`, `absolute_path`).
- A Picker task (`cx.spawn_in` on the picker) dies with the modal; spawn follow-up work with `window.spawn(cx, ..)` and `.detach_and_notify_err(workspace, window, cx)` (`NotifyTaskExt`, `notifications.rs:1698`).
- Picker delegate with a "naming" second step: `cx.defer_in(window, |picker, w, cx| { picker.set_query("", w, cx); picker.refresh_placeholder(w, cx) })` from `confirm`; `update_matches` then stores the query as the name. `fuzzy_nucleo::match_strings` (sync, sorted) is fine for ~12 candidates.
- `Picker` modal presentation already gets the Zenith search field under `IslandsActive` (`picker/src/render.rs:460`); `initial_width(rems(20.))` sets the width; no wrapper needed.
- `fs` is only needed as a dev-dep for tests (`as_fake`, `Fs::load`); `Arc<dyn Fs>::metadata` needs no import.
