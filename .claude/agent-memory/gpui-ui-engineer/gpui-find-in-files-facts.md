---
name: gpui-find-in-files-facts
description: Verified picker/preview/key-context facts from rebuilding zenith_search Find in Files (fork sha b4130a774e)
metadata:
  type: project
---

- `Picker::embedded()` still sizes itself to `DEFAULT_MODAL_WIDTH` 34rem (`crates/picker/src/picker.rs:45`, `shape.rs:210`), narrower than a wider wrapper card; and its list max-height is clamped UP to `min_results.height` 320px (`shape.rs:245`), so a short fixed-height list cannot be had from `Picker`. Own the list (`uniform_list` + `UniformListScrollHandle`) in the modal instead.
- Keymap binds up/down/escape/tab only in `"Picker > Editor"` (`assets/keymaps/default-macos.json:1298`). A hand-rolled modal gets them with `.key_context("MyName Picker")` (one element, two identifiers) plus `on_action` for `menu::{SelectNext,SelectPrevious,SelectFirst,SelectLast,Confirm,SecondaryConfirm,Cancel}` and `picker::ConfirmCompletion` (tab).
- `picker_preview::editor_preview(project, window, cx) -> Arc<dyn PreviewBackend>` works standalone (no Picker): `.update(PreviewUpdate::from_buffer(buf, MatchLocation{anchor_range, range}), window, cx)`, `.render(PreviewLayout::Below, cx)` in a fixed-height div, `.clear(cx)`, `.adjust_to_new_size` after the editor was drawn (call it two `window.on_next_frame` hops later to centre the match). Crate: `picker_preview` (in-workspace dep).
- `render_*` helpers returning `impl IntoElement` that borrow `cx` need `+ use<>` or the next `cx.listener` hits E0502 (Rust 2024 capture rules).
- Test helpers on a modal must be `pub(crate)` + `#[cfg(test)]`; fields stay private to the module. A `cx.on_action(|a: &DeploySearch, _| ..)` global catches `window.dispatch_action` when the `search` crate is not initialised.
- `PathMatcher` include globs: a plain `dir` matches by path prefix; mask inside a dir = `dir/**/*.php` (globset `/**/` matches zero dirs) (`crates/util/src/paths.rs:827,917`).
