---
name: gpui-diagnostics-panel-facts
description: Verified fork APIs for reading diagnostics, panel set_active trap, and test setup (zenith_problems, fork b4130a774e, 2026-11-19)
metadata:
  type: reference
---

Verified in fork `~/GithubProjects/zed` @ b4130a774e (feat/look), 2026-11-19:

- Diagnostics from a buffer: `BufferSnapshot::diagnostics_in_range::<_, Point>(0..snapshot.len(), false)` (`crates/language/src/buffer.rs:5276`) yields `DiagnosticEntryRef{range, diagnostic}`; `diagnostic.is_primary`, `.severity` (`lsp::DiagnosticSeverity` consts), `.message.as_str()`.
- Files with errors without opening buffers: `Project::diagnostic_summaries(false, cx)` (`project.rs:5543`) -> `(ProjectPath, LanguageServerId, DiagnosticSummary{error_count, warning_count})`; one row per server, so dedupe paths. `Project::diagnostic_summary(false, cx)` gives totals. `project::Event::DiagnosticsUpdated{paths, language_server_id}` (`project.rs:395`).
- Jump: `Workspace::open_path(path, None, true, window, cx)` -> `Box<dyn ItemHandle>`, `.downcast::<Editor>()`, then `Editor::go_to_singleton_buffer_point(Point, window, cx)` (`editor/src/navigation.rs:991`). Needs no buffer kept alive.
- Panel `set_active` runs INSIDE a workspace update (dock activation): reading the workspace there panics ("cannot read Workspace while it is already being updated"). Use `cx.defer_in(window, ..)`.
- Test pushing diagnostics: `lsp_store.update_diagnostics(LanguageServerId(0), PublishDiagnosticsParams{..}, None, DiagnosticSourceKind::Pushed, &[], cx)` works with `Project::test` + a worktree, no fake server; `lsp::Diagnostic{message: "..".into(), ..}`.
- Panel test: `init(cx)` then `MultiWorkspace::test_new`; `workspace.panel::<P>(cx)`, `workspace.focus_panel::<P>(window, cx)` opens the dock and focuses; `cx.bind_keys([KeyBinding::new("down", menu::SelectNext, Some("Ctx"))])` + `cx.simulate_keystrokes("down enter")` is the keyboard path. `up/down/enter/home/end` are bound globally in default keymaps (menu::*), left/right only in "menu"/panel contexts.
- Panel position follows settings only (dock observes SettingsStore); a panel without a setting is fixed (`position_is_valid` = Bottom only).
- `ui::Label` has no `px_2` (wrap in `div()`); `CountBadge` is red-tinted; `Panel::icon_label` numeric string is drawn as CountBadge on the dock button when the panel is not active (`dock.rs` ~1608).
- Bottom-dock panel buttons already appear in the Zenith left-rail foot (`zenith_rails` `Rail.foot` = PanelButtons(Bottom)).
