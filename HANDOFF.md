# Zenith — Handoff (work machine → home machine)

Last updated: 2026-11-16 (home machine; repos under `~/GithubProjects/`, not `~/GithubRepos/`). Read with `CLAUDE.md` (project rules) and `plan/README.md` (roadmap).

## 1. Set up the home machine

```sh
# Tools
xcode-select -p || echo "install Xcode (see below)"
brew install gh cmake fswatch
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh   # if no rustup
gh auth login            # smrafiz (daily) — add wp-sigmadevs too if you need admin tasks
gh auth switch -u smrafiz

# Repos
mkdir -p ~/GithubRepos && cd ~/GithubRepos
git clone https://github.com/wp-sigmadevs/zenith.git
git clone --filter=blob:none https://github.com/wp-sigmadevs/zed.git
git -C zed remote add upstream https://github.com/zed-industries/zed.git
git -C zed switch zenith

# Stock-Zed config layer (plan 03)
zenith/zed-kit/install.sh --dry-run && zenith/zed-kit/install.sh
```

Then merge `zenith/zed-kit/settings.global.jsonc` into `~/.config/zed/settings.json` by hand: PHP `language_servers: ["intelephense","phpactor","..."]`, the twig/dockerfile/make/http extensions, Tailwind `includeLanguages` for php/blade, and `telemetry` off. Claude's Supercharger hook blocks writes to `~/.config`, so you make that edit yourself.

Xcode notes from the work machine:
- The App Store Xcode needs macOS ≥ 26.6. On 26.5, use Xcodes.app (`brew install --cask xcodes`) → Xcode 26.5.0 → Make active.
- Run `sudo` in the real Terminal app, not Claude's `!` prompt (no password prompt there).
- `sudo xcode-select -s /Applications/Xcode-26.5.0.app/Contents/Developer && sudo xcodebuild -license accept`
- `xcodebuild -downloadComponent MetalToolchain` — required; without it `gpui_apple` fails with "missing Metal Toolchain".
- Need ≥ 80 GB free for Xcode plus Zed's `target/`.

## 2. State

| Area | State |
|---|---|
| Plan (32 docs) + GitHub (31 issues, 6 milestones) | ✅ `wp-sigmadevs/zenith` |
| Engineer agents (15) + hooks | ✅ `.claude/agents/`, `.claude/hooks/` — modernized, pushed (`81cba24`) |
| 03 config layer (`zed-kit`) | 🟨 built and installed on the work machine; **not yet verified in a running Zed** |
| Fork | ✅ `wp-sigmadevs/zed` (smrafiz has write). Branches: `zenith` (`76f912fa08`: upstream main + rebrand) · `feat/branding` (`0214f9dbc5`: icon, full rebrand, logo, tagline — merged into `zenith` @ `76f912fa08`) · `feat/rebrand` (`8c4e083700`, now contained in feat/branding) |
| Plan 01 | ✅ run, tests, upstream merge; `script/bundle-mac -i` → `/Applications/Zenith Dev.app` opens (home machine, 2026-11-16) |
| Icon | ✅ `brand/zenith-icon.svg` (layers `background`/`glyph`) + 512/1024 PNGs; swapped into all 8 `crates/zed/resources/app-icon*.png` on `feat/branding` |
| Plan 02 rebrand | ✅ code done, compiled, tests pass, bundle opens — see §2b |
| Plan 32 welcome | 🟨 `feat/welcome` @ `6f77bb386a` pushed; tests + clippy green; awaiting visual check + merge |
| First build `cargo build -p zed` | ✅ on work machine (debug, after installing the Metal Toolchain; first build ≈ 1 h, incremental ≈ 2 min; target/ ≈ 25 GB) |
| `cargo test -p workspace` | ✅ 307 passed (work machine) |
| Toolchain | Rust 1.98.1 (pinned by repo), Xcode 26.5, cmake 4.5 |

## 2b. Rebrand (plan 02) — status

Owner decisions: **full rebrand** ("everything"), **telemetry/crash/auto-update off**, settings **copied once** (done).

`feat/branding` commits on top of the icon commit:
- `9359dfe882` core: `paths.rs` APP_NAME "Zenith" (+ removed main.rs bin-name assert), release_channel display_name + app_id → `io.github.wp-sigmadevs.Zenith*`, URL scheme `zenith://` / `zenith-cli://` (+ Cargo.toml osx_url_schemes), CLI → `/usr/local/bin/zenith`, auto-update off via `.cargo/config.toml` `ZED_UPDATE_EXPLANATION`, telemetry defaults off, DMG `Zenith-<arch>.dmg`, plist strings.
- `04f99cf8a4` + `7ab5ccdbaa`: user-visible "Zed" → "Zenith" (UI strings + settings doc comments). Rule: app/editor → Zenith; Zed's services/company (zed.dev account, Zed AI/Pro, Zed Agent, edit-prediction data, billing, extension registry, Zed Industries) stay "Zed". Kept on purpose: identifiers, `ZED_*` env, `.zed/`, `.zed_server`, zed.dev URLs, HTTP User-Agent, MCP/DAP client names, font/icon/theme names ("Zed Plex/Mono", "Zed Icons"), base keymap "Zed", internal `zed:///` mention URIs and `zed://schemas/` (persisted/internal), Windows-only code.
- `8c4e083700` fix: telemetry test compiled after importing `BorrowAppContext`.
- `057ee02022` logo: `assets/images/zed_logo.svg` + Zed half of `zed_x_copilot.svg` → monochrome Zenith glyph (peak + sun).
- `9e995fb586`, `0214f9dbc5` tagline "IDE depth. Editor speed." (onboarding, welcome, snap summary).

Verified (home machine): `cargo check -p zed` ✅; tests ✅ 785 passed / 0 failed (release_channel, paths, cli, workspace, client, agent_skills, terminal, context_server, zed, title_bar, oauth_callback_server); bundle opens with Zenith name/icon.

Left: Windows instance names still `Zed-Editor-*` (only matters on Windows). Fork README `> [!IMPORTANT]` notice — owner removes it by hand before merging into `zenith`.

Data: on the work machine `~/.config/zenith` and `~/Library/Application Support/Zenith` were copied from Zed (db via `sqlite3 .backup`). On the home machine Zenith was launched first, so it has a fresh data dir; copy Zed's db over it (Zenith quit) if history is wanted.

Name risk: pending USPTO "ZENITH" word mark (Zenith IOS Manager LLC, filed Jun 2025) — goods/services unchecked. Check before any public release.

## 3. Open decisions (owner)

1. Commit prefix in the fork: `feat(<crate>):` (recommended, passes the commit hook) or `zenith(<feature>):` (plans 02/16 say this; the hook rejects it). Then have docs-editor fix plans 02/16.
2. Keep or drop the `<example>` block in agent descriptions (Anthropic's guidance dropped them in Apr 2026).
3. "scratch removed": unclear whether this meant dropping the Scratch files feature (plan 04). Confirm.
4. Plan 22 scope: Zed now isolates agent threads in worktrees upstream. Have lead-engineer shrink plan 22 to the gaps.

## 4. Next steps (in order)

0. Plan 32 welcome screen: built on fork `feat/welcome` (`6f77bb386a`), tests + clippy green, installed as Zenith Dev.app. Owner: visual check, remove README notice; then merge `feat/welcome` into `zenith`.
1. ✅ 2026-11-16: notice removed, `feat/branding` merged into `zenith` (`76f912fa08`), pushed.
2. Commit-prefix decision (§3.1), then close plan 02.
3. Plan 17: sccache, nextest, bacon, line-tables-only debug; record times in `plan/build-log.md`.
4. lead-engineer re-checks the agents' Zed API facts against the real fork source (8 items still marked *verify*).
5. Verify plan 03 in Zed (checklist in `zed-kit/README.md`) → mark ✅, close its issue.
6. Plan 15 `zenith_core` → Phase 1 (04 scratches?, 14 toolbar, 05 local history…).

## 5. Gotchas

- Commits must be conventional (`docs:`, `feat(x):`, `fix:`, `chore:`); a hook rejects others.
- Claude's auto-mode may block `git push` to a public repo unless you ask for it explicitly in chat.
- Supercharger blocks writes under `~/.config/` and creating `.claude/hooks/` from Claude; do those yourself.
- Project agents load only in sessions started inside `~/GithubRepos/zenith`. Start Claude there, or symlink `.claude/agents` and `.claude/hooks` into the fork.
- Admin on a personal-account repo can't be granted to collaborators; do admin tasks as `wp-sigmadevs` (`gh auth switch -u wp-sigmadevs`).

## 5b. Resume prompt for Claude

```
cd ~/GithubRepos/zenith && claude
> Read HANDOFF.md and CLAUDE.md. Continue §2b: finish the Zenith rebrand on feat/rebrand in ../zed, build, test, bundle.
```
