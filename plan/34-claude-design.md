# 34 — Claude Design: implementing the target look

Status: ⬜ plan (2026-11-17) — run `lead-engineer` on each step before code.

## Goal

Make the running editor match `mockups/claude-design/` (11 boards, Driftwood dark). One board at a time, cheapest wins first, language server or extension before fork code, fork code in `zenith_*` crates behind one-line upstream hooks (plan 02).

## Decided

- Default look: theme Driftwood + icon theme Archipelago Icons (plan 14, mockups session 2026-11-17).
- Colour roles: blue = the IDE, orange `#ff7a3d` = anything an agent did. Warnings must not look orange — warning colour gets its own hue (amber/yellow) via theme override.
- One scene per screen: agents stay in the title-bar chip until they need you (boards 1, 4).
- `zenith-v1.html` is a feature inventory only; `zenith-v2.html` and `claude-design/` are the target.

## Boards → owner

| Board | What it needs | Built from | Fork cost | Plan |
|---|---|---|---|---|
| 11 Components | Tokens: buttons, pills, status dots, tab states (incl. "pending agent changes", review tab) | Theme overrides first; `ui` component variants only where a theme token is missing | Low | 14 |
| 1 Editing — title bar | Project badge, branch, Search Everywhere box (⇧⇧), run config + run/debug, agent chip "1 running · review 2" | New `zenith_title_bar` crate, one hook in upstream `title_bar`; run config from Zed tasks | Low | 14 |
| 1 Editing — editor | Inline WP warning under the line, parameter-name hints, hook icons in the gutter | WP rules = diagnostics from `wp-hooks-ls`, shown by Zed inline diagnostics; hints from Intelephense inlay hints; gutter icons need a fork hook (*verify*: no extension API for custom gutter icons) | None / Medium | 19 |
| 7 Hook hover | Listener list across plugin + active theme | `wp-hooks-ls` hover — no fork | None | 19 |
| 5 Search Everywhere | One modal: classes, files, symbols, WP hooks, actions | `zenith_search` modal reusing file finder, project symbols, command palette pickers; hooks source from `wp-hooks-ls` workspace symbols | Medium | 14 |
| 4 Agent popover | Chip opens a short task list | Part of `zenith_title_bar`; data from plan 22 task model | Low (after 22) | 22 |
| 3 Agent review | One review tab per task, accept/reject per hunk, run tests in worktree, accept/reject all | Zed's agent diff multibuffer (*verify* it can target a worktree branch) + plan 22 worktrees | Medium | 22, 23 |
| 6 Inline agent edit | Pending agent hunk inline, accept/reject in place | Zed's inline agent diff already does this for its own agent (*verify*); extend to external agents (Claude Code, Codex) via plan 06 | Medium | 06, 23 |
| 2 Debugging | Xdebug paused, inline values, frames/variables bottom | Zed debugger + PHP extension Xdebug adapter; mainly default dock layout | Low | 03 |
| 8 Run | PHPUnit in Docker, green gutter run icons per test | Runnables via tree-sitter `runnables.scm` (exists for PHP *verify*); results panel = plan 07; Docker = plan 11 | Medium | 07, 11 |
| 9 Tool windows | Left/right **stripes** with panel icons, overflow for Tests/Scratches/Bookmarks/Composer/DB | Zed has dock buttons in the status bar only — stripes need upstream workspace changes | High | 14 |
| 10 Narrow | <900 px panels overlay the editor; <500 px title bar icons only | Upstream workspace/dock layout | High | 14 |
| — Islands | Rounded, separated panels | Upstream workspace/pane styling; merge cost on every upstream sync | High | last, owner decides |

## Order

1. **Look** (board 11): bundle Driftwood + Archipelago Icons as defaults, theme overrides for warning hue and agent accent. Settings/assets only.
2. **Title bar** (board 1, top): `zenith_title_bar` with badge, branch, Search box (opens existing finder until step 4), run config, agent chip (static until plan 22).
3. **Editor** (boards 1, 7): `wp-hooks-ls` diagnostics + hover; turn on inline diagnostics and inlay hints by default; then decide the gutter-icon fork hook.
4. **Search Everywhere** (board 5).
5. **Agents** (boards 3, 4, 6): after plans 22/23.
6. **Debug and Run** (boards 2, 8): layout defaults, then plan 07.
7. **Stripes, Narrow, Islands** (boards 9, 10): only after measuring the upstream diff each needs; owner decides.

## Per-board method

1. Read the board (`mockups/claude-design/<Board>.dc.html`).
2. List what Zed already does; note the gap.
3. Place each piece: language server → `zenith_*` crate → one-line upstream hook.
4. Build, test, clippy.
5. Compare: headless-Chrome screenshot of the board vs a screenshot of the running app.

## Open

- Gutter hook icons: extension API or fork hook? Check Zed source before step 3.
- Agent review on a worktree branch: does Zed's agent diff support it, or does plan 23 need its own view?
- "Accept all" is the primary orange button on board 3/11 — owner to confirm it should not be neutral (risk: accept without reading).
- Stripes/Islands: worth the merge cost? Measure the upstream diff first.
