# 02 — Fork Architecture & Conventions

Principle: **all zenith code lives in new crates**; upstream files get only one-line hooks. That keeps weekly merges cheap.

## Layout

```
crates/
  zenith/               # umbrella: zenith::init(cx) calls every feature's init (Cargo feature per crate, see 17)
  zenith_core/          # shared infra: process, paths, store, jobs, mcp, ui, detect (see 15)
  zenith_scratches/
  zenith_local_history/
  zenith_ide_server/
  zenith_test_runner/
  zenith_http/
  zenith_refactor/
  zenith_git_merge/     # or patches inside git_ui if unavoidable
  zenith_db/
```

Upstream touch points (target: ≤ 5 lines total across upstream files per feature):
- `Cargo.toml` workspace members (auto via `crates/*` glob? *verify*).
- `crates/zed/Cargo.toml` → depend on `zenith`.
- `crates/zed/src/main.rs` → `zenith::init(cx)`.
- `crates/zed/src/zed.rs` → register panels where other panels are loaded (*verify*: `initialize_panels` / `load_panels`).
- `assets/keymaps/default-macos.json` → avoid; ship our own keymap file merged at init if possible.

## Zed building blocks (verify each against current source)

| Need | Zed mechanism |
|---|---|
| Dockable panel | `workspace::Panel` trait (+ `Focusable`, `Render`, `EventEmitter<PanelEvent>`) — copy `outline_panel` as template |
| Center tab/view | `workspace::Item` trait — e.g. diff views, HTTP response, DB grid |
| Commands | `actions!(namespace, [Foo, Bar])` + `cx.on_action` / `workspace.register_action` |
| Settings | `settings::Settings` impl + JSON schema; read with `MySettings::get_global(cx)` |
| Persistence | `db` crate (SQLite via `sqlez`), `define_connection!` style migrations |
| Buffer/file events | `project::Project` / `BufferStore` events (e.g. saved, reloaded) |
| File system | `fs::Fs` trait (works for local + remote) |
| Running processes | `task` crate / terminal for user-visible; `smol::process` / `util::command` for background |
| LSP access | `project.lsp_store()` requests (code actions, workspace edits) |
| Git | `git` crate (repo ops), `git_ui` (UI) |
| UI components | `ui` crate (`ListItem`, `Button`, `Tooltip`, `ContextMenu`, `Table`?) |
| Feature gating | `feature_flags` crate or our own setting `zenith.<feature>.enabled` |
| Tests | `gpui::TestAppContext`, `project::FakeFs`, `#[gpui::test]` |

## Conventions

- Setting namespace: `"zenith": { "<feature>": { ... } }` in `settings.json`.
- Action namespace: `zenith_<feature>::*`, all discoverable in command palette.
- Every feature: on/off setting, default **on** in our fork.
- Every feature crate: unit tests + at least one `#[gpui::test]` UI smoke test.
- Commit prefix: `zenith(<feature>): ...`.
- Each feature doc in `plan/` updated to ✅ with "Implemented in" crate path + notes on deviations.

## Feature doc template

Every plan file 04–12 follows: Goal · Parity checklist · UX · Architecture · Data & settings · Actions & keymap · Milestones · Tests · Risks/open questions · Effort.
