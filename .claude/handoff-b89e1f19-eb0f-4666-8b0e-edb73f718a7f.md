## Handoff — Zenith — 2026-11-16

### Done
- Home machine set up: Xcode 26.5 active (`/Applications/Xcode-26.5.0.app`), Metal Toolchain 17F42 installed. Repos at `~/GithubProjects/{zenith,zed}` (not `~/GithubRepos`).
- Rebrand (plan 02) finished on fork `feat/branding` @ `0214f9dbc5` (pushed): reviewed core + WIP commits, finished strings (`7ab5ccdbaa`), fixed telemetry test (`8c4e083700`), Zenith logo vectors (`057ee02022`), tagline "IDE depth. Editor speed." (`9e995fb586`, `0214f9dbc5`). `feat/rebrand` @ `8c4e083700` pushed.
- `script/bundle-mac -i` → `/Applications/Zenith Dev.app` launches; user screenshot confirms Zenith name + new logo.
- Docs pushed: `c22b34b` (plan/README bundle id + plan 01 ✅, HANDOFF §2/§2b/§4, CLAUDE.md status), `0759b20` (plan/32-welcome-screen.md brief).

### In Flight
- Welcome screen (plan 32): brief agreed, **plan not written** — the lead-engineer run was stopped by shutdown. Rerun it from `plan/32-welcome-screen.md`.
- Installed app predates the tagline commits (shows the old tagline); next bundle build picks it up.

### Decisions Made
- One PhpStorm-style screen replaces both onboarding and welcome: owner choice (screenshot review).
- Welcome requirements 1–7 in plan/32 (Projects default, no telemetry toggles, Claude/Codex first, framework badges, bolder logo): owner said "yes" to recommendations.
- Tagline "IDE depth. Editor speed.": owner accepted recommendation.
- Rebrand keep-as-"Zed" rule (services, User-Agent, MCP/DAP client names, fonts/icons/themes, base keymap "Zed", internal `zed:///` + `zed://schemas/` URIs, Windows-only code): recorded in HANDOFF.md §2b.
- Logo swap done by replacing `assets/images/zed_logo.svg` contents (keeps `VectorName::ZedLogo`, zero code hooks).

### What Failed
- `sudo` via `!` prompt: no TTY for the password → run sudo in Terminal.app.
- Telemetry test patch `SettingsStore::update_global` / then `cx.update_global` without the `BorrowAppContext` trait: didn't compile; fixed by importing `gpui::BorrowAppContext as _`.
- Write tool to the fork path: blocked by Supercharger (outside project root) until `.supercharger.json` `additionalRoots` was added.
- zsh `"$R:crates/…"` parsed `:c` as a history modifier → use `"${R}:path"`.

### Blockers
- Merge `feat/branding` → `zenith`: owner must first remove the fork README `> [!IMPORTANT]` notice (fork CLAUDE.md rule).

### Worktrees
- none (zenith: main only; zed: feat/branding only)

### Files Touched
- `plan/README.md`, `HANDOFF.md`, `CLAUDE.md`: status → rebrand done (`c22b34b`).
- `plan/32-welcome-screen.md`: new welcome-screen brief (`0759b20`).
- `.supercharger.json` (untracked, machine-specific): `additionalRoots` → `/Users/srafiz/GithubProjects`.
- Fork: see commits listed under Done.

### Resume With
Read HANDOFF.md and plan/32-welcome-screen.md. Run lead-engineer on plan 32 against the fork at ~/GithubProjects/zed (branch feat/branding), show me the plan before any code.

### Start With
none — no conflict or guard state pending.

### Measurements
- `cargo check -p zed` (home machine, first run, Rust 1.98.1, Xcode 26.5): 11m 13s.
- Tests on feat/rebrand @ `8c4e083700`: `-p release_channel -p paths -p cli -p workspace -p client -p agent_skills -p terminal -p context_server` → 630 passed, 0 failed; `-p zed -p title_bar -p oauth_callback_server` → 155 passed, 0 failed, 1 ignored (only 2 result lines printed; title_bar may have 0 tests).
- First `bundle-mac -i`: log started 00:05:40 (+06); zed binaries 11m 10s; remote_server 7m 49s; end time not recorded (≈25 min, estimate).
- Disk free: 79 GiB before Xcode, 73 GiB after.

### Rejected — do not rebuild
- Renaming internal `zed:///agent/...` mention URIs and `zed://schemas/...`: they are persisted in thread history / internal to the JSON LS; renaming breaks saved threads.
- Renaming font/icon/theme names ("Zed Plex", "Zed Mono", "Zed Icons", "Zed (Default)") and base keymap "Zed": they are asset/settings identifiers.
- Fixing `bundle-mac -i` exit 1: upstream script bug (after install it `mv`s the already-moved app for the DMG); app is fine; left to avoid an upstream touch.

### Dead ends
- none

### Open questions
- Who pushed `7ab5ccdbaa` to origin/feat/rebrand before my push (remote already had it)? Unverified; push was a clean fast-forward.
- Does `title_bar` have any tests? Unverified.
- Copying Zed's db into Zenith on the home machine: not done; Zenith already created a fresh data dir.

### Reproduce
```
cd ~/GithubProjects/zed && git switch feat/branding
cargo check -p zed
cargo test -p release_channel -p paths -p cli -p workspace -p client -p agent_skills -p terminal -p context_server
cargo test -p zed -p title_bar -p oauth_callback_server
./script/bundle-mac -i   # exits 1 after "Installed application bundle" — expected
```
