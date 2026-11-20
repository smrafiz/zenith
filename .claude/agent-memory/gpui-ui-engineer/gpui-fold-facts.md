---
name: gpui-fold-facts
description: Verified editor fold / item-added / test-harness API facts for zenith_folds (fork feat/look, 2026-11-20)
metadata:
  type: reference
---

- Persisted folds load synchronously in `Item::added_to_workspace` (`editor/src/items.rs:1136`, `fold.rs:1056 load_folds_from_db`), which runs before `workspace::Event::ItemAdded` (`workspace.rs:6435`). Decide "does the editor have folds" from an `ItemAdded` subscriber, not at `observe_new::<Editor>` time. `Editor::workspace()` is `None` until then.
- `fold_ranges(Vec<Range<T: ToOffset>>, auto_scroll, window, cx)` `fold.rs:626`; `Point` ranges work on singleton editors. `folds_did_change` persists folds to the `file_folds` DB table, so the auto-fold is saved too; an unfold-then-close deletes it and the next open folds again.
- Fold chip: `FoldPlaceholder::fold_element` (`fold_map.rs:~57`) already sets `.hover(..)`; gpui panics `hover style already set` (div.rs:867) on a second `.hover` in a rendered test. Driftwood `element.background` (#2b2d30) is nearly invisible on the editor (#282c34); `element_hover` (#ffffff17) is a visible chip.
- No tree-sitter-php in the workspace; PHP grammar is only `php.wasm` in the installed extension (node kind `namespace_use_declaration` confirmed via `strings`). Tests use `tree-sitter-typescript` (`LANGUAGE_TYPESCRIPT`), `LanguageConfig.matcher` needs `.into()`.
- Syntax tree: `BufferSnapshot::syntax_layers()` -> `layer.node()` (tree_sitter::Node) and `layer.language.name()`; `EditorEvent::Reparsed` fires on reparse and language change.
- Test editor from `workspace.open_path` then `active_item_as::<Editor>`; buffer edits without a window: `editor.buffer().update(cx, |b, cx| b.edit([(range, text)], None, cx))` (`update_in` needs a VisualTestContext). `observe_new::<Editor>` registered before the crate's `init` can stand in for restored state (folds, selection).
