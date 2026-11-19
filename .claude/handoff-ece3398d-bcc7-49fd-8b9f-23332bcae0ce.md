## Handoff — Zenith — 2026-11-19 (home machine, evening)

### Done
- Home toolchain: Xcode 27.2 active (26.5 kept for rollback), sccache/nextest/bacon/cargo-sweep/fswatch installed; `~/GithubProjects/.cargo/config.toml` sets sccache for that folder only.
- Upstream sync (plan 13): `main` ff to upstream `4a7d10473a`, merged into `zenith` (`a29abb9ed4`, 2 conflicts resolved: `client/zed_urls.rs`, `onboarding/onboarding.rs`), `zenith` merged into `feat/look`; log in `plan/sync-log.md`; rerere on. All pushed.
- Fork `feat/look` (pushed, head `b4130a774e`), by commit: `2b63f7875f` Lucide icons (rails, panels, Agents chip, ISC notice `assets/icons/LICENSE-LUCIDE-zenith.txt`); `2b0776d98f`+`a9b217efe1` `zenith_splash` startup card (hold ≥1.5 s, "Zenith Dev 1.31.0"); `393a240cc6`+`5ca0ddc785` Project header buttons and ⋮ menu (Behavior, Appearance, Sort By, Move to, Resize, Remove from Sidebar) + ⌥⌘←/→ Back/Forward in `assets/keymaps/zenith.json`; `6dd0f56206` draggable Search Everywhere/Recent Files popup + PhpStorm look; `ca1cd78178` drag rail buttons between rails, terminal docks right; `7b1fe2739a` tree context menu in PhpStorm order, green test rows / brown ignored rows; `773d1ef283` pinned tabs in a separate top row; `b4130a774e` Find in Files / Replace in Files popup on ⌘⇧F/⌘⇧R.
- Tests: zenith crates + icons 103/103 on the synced tree; later runs: zenith_search 20/20, workspace pane 134/134, terminal_view 99/99, project_panel context/zenith tests pass.
- zenith repo `main` (pushed `6d1ac43`): `plan/sync-log.md`, `plan/visual-check-2026-11-19.md` re-check, `mockups/zenith-splash.html`, HANDOFF row.

### In Flight
- Release bundle of `b4130a774e` was building in background (`script/bundle-mac -i`, log in the session scratchpad `bundle4.log`) when this brief was written; not confirmed finished. Dev profile was cleaned first (69 GiB free).
- Nothing else uncommitted in the fork. zenith repo: this brief + notes below uncommitted until the commit that adds it.

### Decisions Made
- Keep Claude Design's wide centred search pill (real IDEs use a small right-hand magnifier).
- Owner choices that are NOT differences: indent-guide background colouring, inline git blame, parameter hints, fonts 16/17/1.8.
- Tool-window menu: only entries Zenith has a feature for; left out Edit Scopes, Group Tabs, View Mode, Help (say so, don't show dead items).
- Replace happens in the Project Search tab; the ⌘⇧R popup hands the query over ("Open in Find Window").
- GitHub login + settings sync = plan 33; recommended first slice: device-flow login, settings in a private repo `zenith-settings` (not gist), token in keychain. Owner has not answered repo-vs-gist or which OAuth app. Stop and confirm before any auth code.

### What Failed
- Auto-mode classifier blocked one `git commit && git push` chain for the zenith repo; committing locally then pushing on an explicit "push" worked.
- `sed -i` without `''` on macOS; zsh `set -- $b` does not word-split (use `read`). A python edit chain that dropped a `)` broke a `.child(` block once (fixed with the Edit tool).
- First splash capture looked see-through (fade-in); later frame was fine; a 4th frame already showed the workspace (splash gone <1 s before the 1.5 s hold fix).

### Blockers
- Owner: open ⌘E, ⇧⇧, ⌘⇧6, the Project ⋮ menu, ⌘⇧F/⌘⇧R and drag a rail icon in the new app and send screenshots; Claude cannot send keystrokes.
- Owner: `~/.config/zenith/settings.json` PHP edit (Claude cannot write `~/.config`): text in `plan/visual-check-2026-11-19.md`.
- Owner answer on plan 33 repo-vs-gist.

### Worktrees
- none (zed and zenith: main checkout only)

### Files Touched
- see commit list above. zenith repo this session: `plan/sync-log.md`, `plan/visual-check-2026-11-19.md`, `HANDOFF.md`, `mockups/zenith-splash.html`, `docs/guides/fork-findings.md`, this brief.

### Resume With
Read HANDOFF.md, CLAUDE.md and this brief. Check the bundle finished (`ls -ld "/Applications/Zenith Dev.app"`, stderr of a launch), then ask the owner for screenshots of the modals/header/⋮ menu and fix what differs; build only when asked in that message.

### Start With
- /sc-status — confirm guards and disk (`df -h ~` ≥ 30 GiB) before any test or bundle.

### Measurements
- Bundles on this machine: 19m33s (2142 s user build before splash), 16m43s, 15m00s (2067.89 s user), all warm with sccache; the old "≈2.5 h after settings/workspace edits" is the work machine without sccache.
- `cargo check -p zed` after the sync: 1m14s, 0 errors; zenith nextest 103 tests 1m41s.
- Disk: 66 GiB → 45 after check; test runs −10 to −17 GiB each; `rm -r target/debug/incremental` freed 11–24 GiB; `cargo clean --profile dev` freed 38.0 GiB (32 → 69 GiB).

### Rejected — do not rebuild
- Generated icon packs (owner rejected earlier); Lucide glyphs from the mockup are the icon source for rails/header.
- A new account service for settings sync as the first step (hosting, licensing, plugin store) — plan 33 first slice is GitHub-only.

### Dead ends
- `webstorm` MCP server: ECONNREFUSED the whole session; use window screenshots instead.
- Sending keystrokes to open modals: blocked.

### Open questions
- Does the new bundle start without a panic and show the splash, rail icons, header, drag-to-rail, tint rows, pinned row, Find in Files popup? (unverified until the bundle is checked)
- Do ⌥⌘←/→ work from the project panel focus (tested only editor/terminal contexts + JetBrains keymap)?
- Do Resize ▸ Stretch entries behave at window edges (40 px step, untested)?
- Splash first frame looked translucent: fade-in or a transparent-window bug (unverified).

### Reproduce
- Zenith tests: `cd ~/GithubProjects/zed && cargo nextest run --no-fail-fast -p zenith_inspections -p zenith_look -p zenith_php_tools -p zenith_rails -p zenith_search -p zenith_title_bar -p zenith_todo -p zenith_welcome -p zenith_splash -p icons`.
- Launch and capture stderr: `RUST_BACKTRACE=1 "/Applications/Zenith Dev.app/Contents/MacOS/zed" <path> > run.log 2>&1`; screenshots: see memory `screenshot-running-app`.
- Mockup render: Chrome headless `--window-size=1600,1000 --screenshot` on `mockups/claude-design/Main.dc.html`.
