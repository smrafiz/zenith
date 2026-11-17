## Handoff — Zenith (plan 34, Claude Design) — 2026-11-17

### Done
- Fork `wp-sigmadevs/zed` branch `feat/look` pushed @ `fae7a95a0c` (from `zenith` @ `2800023217`). Plan 34 steps 1, 2, 3a, 4a, 6a — commit table in `plan/34-claude-design.md` §Progress.
- Step 4a (this session's last work): `crates/zenith_search` — Search Everywhere modal, tab strip (only Actions live), ⌘⇧A / Ctrl+Shift+A, background fuzzy match, history shared with the command palette.
- Zenith repo: plan 34 §Progress, CLAUDE.md status + findings, HANDOFF.md state/next step.

### In Flight
- none mid-edit. Next planned: step 4b (Files source in Search Everywhere, then move ⇧⇧ and the title bar box from the file finder to it).

### Decisions Made
- All Zenith title bar UI is ONE section (`zenith_title_bar::middle`): upstream `ArrayVec<_, 5>` overflowed when the banner shows.
- ⇧⇧ and ⌘⇧A live in `assets/keymaps/zenith.json`, loaded after the base keymap: wins over JetBrains' `command_palette::Toggle` without editing upstream keymaps.
- ⇧⇧ stays on the file finder until 4b: moving it to an Actions-only modal would lose file search.
- Search Everywhere shares the command palette's history via a block appended to `command_palette.rs` (no upstream line changed) — sync-conflict risk was flagged by the owner.
- Picker wrapped in a modal with `.embedded()`: `render_header` hides when there are no matches and sits under the query box.
- Upstream tests that assumed old defaults are pinned to the old value inside the test, not reverted.

### What Failed
- Separate title bar pushes for 2b/2c → `CapacityError: insufficient capacity` at `title_bar.rs:398` (I caused it; fixed in `315b12f9b1`).
- ⇧⇧ in upstream default keymaps (`ebebfae4f2`) → conflicts with plan 02; moved to zenith.json (`b2d94bee7e`).
- Test loading `default-macos.json` → `didn't find an action named "debugger::Start"`; tests can only load keymaps whose actions they link.
- `cargo fmt -p zed` reformatted unrelated files → reverted, formatted all in `ccbadd9716`.

### Blockers
- Visual check: needs a merge of `feat/look` + app rebuild (≈50 min incremental) — owner decides when.
- 3b needs `wp-hooks-ls` (plan 19); 3c gutter hook is an owner decision.

### Worktrees
- none (only `~/GithubRepos/zed` main checkout on `feat/look`).

### Files Touched
- `crates/zenith_search/*` (new), `crates/zenith/{Cargo.toml,src/zenith.rs}` (feature `search`), `crates/command_palette/src/command_palette.rs` (appended block), `assets/keymaps/zenith.json` (⌘⇧A), `crates/zenith_welcome/src/zenith_welcome.rs` (⇧⇧ test moved out). Earlier steps: see `git log zenith..feat/look`.

### Resume With
Start Claude in `~/GithubRepos/zenith`, read HANDOFF.md, CLAUDE.md and this brief; then do plan 34 step 4b in the fork (`~/GithubRepos/zed`, branch `feat/look`): add a Files source to `crates/zenith_search` modelled on `crates/file_finder`, test first, then move ⇧⇧ and the title bar box to `zenith_search::Toggle`. Check `df -h` (≥30 GiB) first; never rebuild or push unless asked.

### Start With
- none — no conflict, guard or stale state pending.

### Measurements
- Disk: 35 GiB free at end; `target/debug` 39 GiB, `target/release` 4.5 GiB. `cargo clean -p title_bar zenith_title_bar zenith_welcome command_palette zenith_search git_ui project_panel agent_ui zed` removed 775 files, 3.9 GiB.
- `cargo test -p zed` ≈ +18 GiB (44 → 22 GiB free, earlier 2026-11-17).
- Tests at end: `zenith_search` 2 passed, `command_palette` 21, `zenith_welcome` 16; clippy clean on all three. Earlier this session: `zenith_title_bar` 2, project_panel 147, git_ui 213, workspace 307 (with the two pinned tests).
- Regression proofs: removing `window.dispatch_action` in confirm, `record_command_invocation`, or the `secondary-shift-a` binding each makes a `zenith_search` test fail.

### Rejected — do not rebuild
- Editing upstream default keymaps for ⇧⇧: plan 02 conflict surface; zenith.json does the same with zero upstream keymap lines.
- Refactoring the palette's own `command_usage`/confirm to share code (`898e214e14`): 63-line upstream diff; replaced by an appended 28-line block (`fae7a95a0c`).
- Picker `render_header` for the tab strip: disappears with zero matches.
- Matching on the UI thread: replaced by background `match_strings_async`.

### Dead ends
- `git log -S` in the fork warns "could not fetch … from promisor remote" (partial clone); use `git grep` on the tree instead.

### Open questions
- Unverified: does the full app start with zenith.json (⌘⇧A) loaded? `cargo tree` shows `zenith_search` linked into `zed`, so the action exists; `cargo test -p zed` not run (disk floor). Settled by the next rebuild or an approved `cargo test -p zed`.
- Unverified: upstream flaky `agent_ui` `test_migrate_thread_remote_connections_backfills_from_workspace_db` — suspected shared test KVP DB.
- Owner: Driftwood info colour `#e5c07b`; README notice removal; plan 31 slice; 3c gutter hook; turning off incremental builds.

### Reproduce
- `cd ~/GithubRepos/zed && cargo test -p zenith_search -p command_palette -p zenith_welcome -p zenith_title_bar`
- `./script/clippy -p zenith_search -p command_palette -p zenith_welcome`
- `git diff zenith..feat/look --stat` (whole plan 34 diff)
