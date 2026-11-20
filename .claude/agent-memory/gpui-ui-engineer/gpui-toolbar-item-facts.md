---
name: gpui-toolbar-item-facts
description: Verified workspace/GPUI facts for adding a toolbar item (zenith_markdown, fork b4130a774e + uncommitted)
metadata:
  type: reference
---

- `Toolbar::item_of_type::<T>()` (crates/workspace/src/toolbar.rs:238) finds an added item; tests use it to get the switcher. `ToolbarItemView::set_active_pane_item` can be called directly in tests to read the location.
- `observe_new::<Workspace>` with a window fires for `MultiWorkspace::test_new` workspaces in tests, so `init()` wiring is testable end to end.
- Never call `workspace.update` from inside a toolbar item's own `cx.listener`/update: pane changes update the toolbar item (leased) -> panic. Use `IconButton::on_click(move |_, window, cx: &mut App|)` with owned clones.
- `CloseAndReturnToEditor` is handled by the preview's Render only when it holds focus: focus `item_focus_handle` then `window.dispatch_action`. It defers its own work; chain a second `window.defer` to run after it.
- `MarkdownPreviewView::is_previewing` is private; match previews by `act_as::<Editor>` -> `buffer().as_singleton()`.
- Language of a freshly opened buffer can arrive late: observe the editor and emit `ToolbarItemEvent::ChangeLocation`.
- Tests: `db::AppDatabase::test_new()` global + `AppState::test` + `editor::init` + `markdown_preview::init`; `LanguageConfig.matcher` needs `Arc::new`.

Composite item / toolbar facts (zenith_markdown split view, fork b4130a774e + uncommitted):
- `Toolbar::render` (crates/workspace/src/toolbar.rs:110-160): left/right groups use `justify_between`; with ONLY right items the right group lands at the LEFT edge. Any PrimaryLeft item (even an empty div) fixes it. Breadcrumbs is the usual left item; previews have none.
- `Pane::add_item_inner` (pane.rs:1229) dedups Singleton items by `project_entry_ids().first()` and, when it matches an existing tab, MOVES/replaces it (index shifts, `Some(existing_index)` activates the OLD item). To swap an item in place: `remove_item(old)` first, then `add_item(new, .., Some(index))`; restore pin with `set_pinned_count(pinned_count()+1)`.
- `ItemHandle::added_to_pane` (item.rs:750) calls `set_nav_history` + `added_to_workspace` on every AddItem; forward both to the wrapped editor.
- `Workspace::active_item_as` falls back to `act_as`, but `QuickActionBar::active_editor` (zed/quick_action_bar.rs:87) uses exact `downcast::<Editor>()` => wrapper items hide the quick action bar.
- Wrapper items: forward every Item method via `Item::method(editor.read(cx), ..)` (UFCS, Editor has same-named inherent methods); `act_as_type` -> `Item::act_as_type(editor, type_id, &editor, cx)`.
- `MarkdownPreviewView::close_and_return_to_editor` made `pub` (1 upstream line): calling it directly avoids the focus+dispatch_action dance, which needs a rendered frame. It needs the preview to be a pane item.
- Auto-preview (`MarkdownPreviewView::register`) fires on `ItemAdded` for any Editor; re-adding a dirty editor next to its preview is safe (finds the preview, `replaces_editor` false).
- Tests: `item.act_as::<T>(cx)`/`is_dirty(cx)` need `&App`: wrap in `cx.update(|cx| ..)` on TestAppContext.
- Sync-scroll facts (unrun, see zenith_markdown split_view.rs): `EditorEvent::ScrollPositionChanged{local,autoscroll}` emitted at crates/editor/src/scroll.rs:410 only when the anchor changes; `Editor::scroll_position(cx)` (scroll.rs:751) y = top display row; `visible_line_count()` is None until first layout. Preview scroll state is `MarkdownPreviewView.scroll_handle` (made `pub`); gpui wheel listener (div.rs:3429) does NOT stop propagation and notifies the scrolled view, so an ancestor `.on_scroll(..)` sees the already-updated offset. `Markdown::request_autoscroll_to_source_index` (markdown.rs:1029) only scrolls into view with a 3-line margin and has no read-back. `cx.emit` is deferred to effect flush, so a `syncing` bool around an update cannot guard echo events: compare values instead.
- In gpui tests `WindowHandle::update` leases the root view; drawing needs `cx.update(|cx| cx.update_window(handle.into(), |_, w, cx| w.draw(cx).clear(cx)))`.
- Disk gate: target/ grew to ~83G and `df` fell to 19-21Gi mid-session with no cargo running; even `cargo check --tests` costs ~2G. Check df before every cargo call.
