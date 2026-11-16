## Handoff — Zenith — 2026-11-16

### Done
- Plan 32 welcome screen, chunks 0–8, on fork `feat/welcome` (`b219d29edf`..`6f77bb386a`), pushed. Crates `zenith`, `zenith_welcome`; hooks in `crates/workspace/src/welcome.rs`, `crates/zed/src/main.rs`, `crates/zed/src/zed/open_listener.rs`.
- Zed branding removed (owner request): `8083776638` (keymap shown as "Zenith (default)", Zed Agent card dropped, Learn "Editor Documentation"), `73c2c17416` (`IconName::Zenith`, `assets/icons/zenith.svg`), `fdb008e667` (`title_bar.show_sign_in` default false), `bffc425d7b` (palette `zed:` → `zenith:` display; nav left-aligned). All pushed.
- zenith repo: `9700cd8` plan 32 status, `0de602c` plan 33 Zenith accounts brief + plan index rows 32/33. Pushed. This session's notes added to `CLAUDE.md` "Findings worth keeping" and `HANDOFF.md` §4 (uncommitted at time of writing — see In Flight).

### In Flight
- Installed `/Applications/Zenith Dev.app` (17:32) predates `fdb008e667` and `bffc425d7b`: Sign In still visible, palette still `zed:`, nav still centered. Rebuild needed (owner said "don't rebuild now").
- Owner visual check of welcome screen; README `> [!IMPORTANT]` notice removal (owner only); merge `feat/welcome` → `zenith`.

### Decisions Made
- No user-visible "Zed" anywhere: owner, 2026-11-16. Prefer display-only/zenith-crate changes over renaming upstream ids (keymaps reference `zed::`).
- Zed Agent (zed.dev) sign-in removed from Customize; Claude/Codex first.
- Own Zenith accounts (GitHub OAuth; settings sync, licensing, plugin store) as a separate service = plan 33. Plinth hosts only the website (`zenith.plinthsites.com`).
- Sign In hidden by default until plan 33 ships (default.json, option A).

### What Failed
- `cargo clean` / deleting `target/release` while clippy ran → `No such file or directory (os error 2)`, CLIPPY_EXIT=101; rerun after clean bundle passed.
- First humanize change returned `"zenith:  open onboarding"` (double space): recursing on the bare name adds a leading space before the capital. Fixed by humanizing `zenith::{rest}`.

### Blockers
- none (waiting on owner: rebuild timing, visual check, JetBrains-import scope).

### Worktrees
- none (only main checkouts: zenith `main`, zed `feat/welcome`).

### Files Touched
- `zed/crates/zenith_welcome/src/customize.rs`: own keymap section (Zenith label/icon, no telemetry); Zed Agent card removed.
- `zed/crates/zenith_welcome/src/view.rs`: dropped `user_store` plumbing; nav buttons not `full_width` (left-align).
- `zed/crates/zenith_welcome/src/learn.rs`: "Editor Documentation".
- `zed/crates/zenith_welcome/Cargo.toml`: `client` → dev-dependency.
- `zed/crates/icons/src/icons.rs`, `zed/assets/icons/zenith.svg`: Zenith icon (upstream enum edit, one line).
- `zed/assets/settings/default.json:638`: `show_sign_in` false.
- `zed/crates/command_palette/src/command_palette.rs`: `zed::` displayed as `zenith:`; test.
- `zed/crates/which_key/src/pending_bindings.rs`: test strings `zenith: open keymap/settings`.
- `zenith/plan/32-welcome-screen.md`, `plan/33-zenith-accounts.md`, `plan/README.md`, `CLAUDE.md`, `HANDOFF.md`.

### Resume With
Read zenith HANDOFF.md §4 step 0/0a and this brief. Rebuild ../zed `feat/welcome` with `script/bundle-mac -i` (~50 min, background), then ask the owner to check the welcome screen and decide the plan 31 JetBrains-import first slice.

### Start With
none

### Measurements
- `cargo clean` (work machine, after plan 32 dev builds): removed 130120 files, 80.1 GiB; free disk 78 GiB after.
- `script/bundle-mac -i` from clean: `Finished release ... in 115m 11s`; full `./script/clippy` right after: 8m 45s, exit 0, no findings; free disk 49 GiB after both.
- Incremental bundle after `8083776638`+`73c2c17416`: release passes 34m 57s + 30.98s + 15m 37s; installed 17:32.
- Tests: workspace 307 pass; zed 148 pass/1 ignored; zenith_welcome 12 pass; icons 2; command_palette 21; which_key 46.
- `bundle-mac -i` always ends BUNDLE_EXIT=1 after "Installed application bundle" (DMG `mv` of already-moved app) — app fine.

### Rejected — do not rebuild
- Renaming action namespace `zed::` → `zenith::`: breaks every user/default keymap and settings that name actions; display-only rename in `humanize_action_name` chosen instead.
- `ListItem` for welcome nav (left-aligned by default): has no `tab_index`, loses keyboard nav; kept `Button` without `full_width`.
- Plinth as the accounts backend: users are CMS editors; no per-user blob store, licences or plugin registry (checked `prisma/schema.prisma` models, `features/`).
- Self-hosting upstream `crates/collab`: needs Postgres + LiveKit ops for features Zenith doesn't need.
- Editing upstream `basics_page.rs` keymap labels: copied the section into `zenith_welcome` instead.

### Dead ends
- No existing Zenith/brand icon in `IconName` (searched for star/sparkle/zen) — had to add one.

### Open questions
- Does the left-aligned nav render as intended? Unverified (needs rebuild + look).
- Does the 16px Zenith icon read well (inner stroke at 0.7 opacity)? Owner saw it render; legibility not judged.
- JetBrains import scope (plan 31 first slice) — owner decision pending.
- Hide or redirect "zenith: get merch" / "zenith: open docs" (still zed.dev) — owner decision pending.

### Reproduce
```
cd ~/GithubRepos/zed
set -o pipefail; cargo test -p zenith_welcome -p command_palette -p which_key -p icons 2>&1 | grep -E "test result|FAILED"
cargo clippy -p zenith_welcome -p command_palette -p which_key -p icons --tests
script/bundle-mac -i   # ~50 min incremental; exit 1 after install is expected
```
