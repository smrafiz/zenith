---
name: gpui-panel-chrome-facts
description: Verified fork facts for in-panel headers, chips, QuickActionBar folding, ItemHandle::act_as (zenith_problems/todo, 2026-11-20)
metadata:
  type: reference
---

Verified in fork `~/GithubProjects/zed` (feat/look), 2026-11-20:

- Dock draws a header only for panels in `zenith_panel_title` (`workspace/src/dock.rs:2192`); others must draw their own. Hide = `window.dispatch_action(workspace::ToggleBottomDock.boxed_clone(), cx)`; test it with `div().debug_selector(..)` around the `IconButton` + `cx.debug_bounds(..)` + `cx.simulate_click(bounds.center(), Modifiers::none())`.
- Dock body already has `panel_background` + rounded border under `IslandsActive` (`dock.rs:1366`): panels need no own background.
- `CountBadge` is `absolute` top/right (`ui/.../count_badge.rs:27`): never put it inline in a row (overlaps labels). Use `Label::new(count).color(Color::Muted)`.
- `ListItem::height(px)`, `.rounded()`, `.indent_step_size(px)`, `.start_slot::<Icon>(Option<Icon>)` (needs the turbofish for an Option). `ButtonLike` has `aria_role`/`aria_label`.
- `FileIcons::get_icon(Path::new(name), cx)` needs `file_icons` dep; `Worktree::read(cx).root_name_str()`.
- `ItemHandle::act_as::<V>(cx)` is on `dyn ItemHandle` (`workspace/src/item.rs:606`) and needs `&App`; `QuickActionBar::active_editor(&self)` has no cx, so cache the result in a field in `set_active_pane_item`.
- A longer condition on an upstream line makes rustfmt re-indent the whole closure (bigger diff): keep the line, filter at the use site (`.children(x.filter(|_| !rails))`).
- Changing `bottom_dock_layout` default needs no test pins: no test references it (grep 2026-11-20).
- Disk: `target/` shared with other agents; free space fell 64 -> 21 GiB in one session. Check `df -h ~` before every test run.
