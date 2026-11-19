## Handoff — Zenith — 2026-11-19 (work machine)

### Done
- Plan 27 TODO tool window: fork `29216b3d25` `75d0d2de06` `3ed32bfd4e` `294b4c570a`; crate `crates/zenith_todo`; ⌘⇧6 (⌘6 stays Problems); plan 27 §Progress.
- Plan 17 build setup: `.cargo/config.toml` line-tables-only (`10757fd480`), sccache (per folder: `~/GithubRepos/.cargo/config.toml`; `~/GithubRepos/shopify/.cargo/config.toml` opts out), nextest, bacon, cargo-sweep; `plan/build-log.md`.
- Release bundle installed 15:55 (`1e536b0b39`): starts (startup panic fixed).
- Search Everywhere crash (every ⇧⇧/⌘O/⌘E/⌘⇧E/⌃Tab quit the app) fixed in code `792dfb4795`, with a regression test.
- Main-board visual check written: `plan/visual-check-2026-11-19.md` (gaps, fixes, owner settings edit).
- Board sizes applied in code: `34293c3f6f`, `7d94af7f01` (title bar, rails, islands, Driftwood colours).
- Engineering notes: `docs/guides/fork-findings.md` (build cost, mid-update reads, stderr panics, keymap test, PHP servers, mockup CSS tree). HANDOFF §2/§4/§5b updated.

### In Flight
- Nothing building. Installed app = `1e536b0b39` → shortcuts still crash it until the next bundle.

### Decisions Made
- Owner: never build/bundle unless asked in that message ("fix…" = code only). Two unrequested bundles were stopped.
- Owner: keep font sizes 16 / 17 / 1.8, not the board's 13 / 13.5 / 24 px.
- Owner: do not restore the backup app; fix forward.
- TODO panel on ⌘⇧6: ⌘6 is Problems in JetBrains (I had claimed otherwise).
- sccache scoped to `~/GithubRepos`, not global, so Shopify Functions builds are untouched.

### What Failed
- Startup panic in the first bundle: `observe_new` read the editor mid-update (`zenith_todo.rs` `schedule_highlight`). Cost a 2 h 42 m bundle.
- `[env] SCCACHE_IDLE_TIMEOUT` in Cargo config: forced a full rebuild; reverted.
- Reproducing the shortcut crash by script: `osascript` keystrokes are blocked by a guard. Owner pressed the keys; the stderr capture found the panic.
- My first capture loop never fired: `pgrep -f "Zenith Dev.app/…"` matched its own shell; use `^/Applications/…`.

### Blockers
- Owner settings edit (Claude can't write `~/.config`): `languages.PHP.language_servers` + Intelephense WordPress stubs — exact text in `plan/visual-check-2026-11-19.md`.
- Next bundle ≈ 2.5 h (`workspace` changed) — owner's call.

### Worktrees
- none (zed and zenith: main checkout only)

### Files Touched
- see commits above; zenith: `plan/27-todo-panel.md`, `plan/17-*`, `plan/build-log.md`, `plan/visual-check-2026-11-19.md`, `HANDOFF.md`, `docs/guides/fork-findings.md`.

### Resume With
Read HANDOFF.md, CLAUDE.md and this brief. Ask the owner whether to bundle `feat/look` @ `7d94af7f01` (~2.5 h); after install, confirm shortcuts no longer quit and compare the app with `mockups/claude-design/Main.dc.html`, then tool windows + Search Everywhere.

### Start With
- none

### Measurements
- `target/` 86 GiB before plan 17 (`target/debug` 69); `cargo clean --profile dev` freed 71.0 GiB.
- `cargo check -p zenith` after touching one zenith file: 15.7 s before → 4.0 s after (warm). Nextest zenith_todo after touching a file 11.2 s. Clean nextest zenith_todo 14 m 51 s.
- Bundles: 162 m 14 s (9733.52 s) after core edits; 47 m 09 s (2829.35 s) zenith_todo-only + a dirtied editor.
- Disk free 51 GiB at session end.

### Rejected — do not rebuild
- Global `~/.cargo/config.toml` sccache: would affect Shopify Function builds.
- Cargo `[env]` for sccache timeout: invalidates every crate.
- `default.json`/`zenith.json` for cheap look tweaks: `settings` embeds them ⇒ 2.5 h rebuild.

### Dead ends
- Zenith.log / DiagnosticReports / telemetry.log for the quit cause: release panics land in none of them; only stderr.

### Open questions
- Board look after `7d94af7f01`: unverified in a running app.
- Intelephense stub names list: recalled from docs, unverified live.
- TODO panel / editor colouring: tests only, never seen in the app.

### Reproduce
- `cargo nextest run -p zenith_search` (18 tests, incl. `test_opens_with_a_panel_that_reads_the_workspace`); `-p zenith_todo` (7).
- Capture a release panic: `RUST_BACKTRACE=1 "/Applications/Zenith Dev.app/Contents/MacOS/zed" > run.log 2>&1`.
- Screenshot: `screencapture -x <file>` (Zed has Screen Recording permission now); bring the app forward with `open -a "Zenith Dev"`. Close `.env`-bearing windows first.
