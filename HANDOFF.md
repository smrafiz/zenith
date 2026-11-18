# Zenith — Handoff (work machine → home machine)

Last updated: 2026-11-19 (home machine; repos under `~/GithubProjects/`, not `~/GithubRepos/`). Read with `CLAUDE.md` (project rules) and `plan/README.md` (roadmap).

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
| Plan (35 docs) + GitHub (32 issues, 6 milestones; README, LICENSE, SECURITY, issue/PR templates) | ✅ `wp-sigmadevs/zenith`; plan 35 PHP toolchain = issue #32 (Phase 3, before 21) |
| Engineer agents (15) + hooks | ✅ `.claude/agents/`, `.claude/hooks/` — modernized, pushed (`81cba24`) |
| 03 config layer (`zed-kit`) | 🟨 installed on both machines (home 2026-11-17: install.sh, WPCS 3.4.1, Phpactor on in `zed-config` `98e70fb`); **not yet verified in a running Zed** |
| Fork | ✅ `wp-sigmadevs/zed` (smrafiz has write). Branches: `zenith` (`0cb9e7432e`: upstream main + rebrand + `.zenith` project dir) · `feat/branding` (`0214f9dbc5`: icon, full rebrand, logo, tagline — merged into `zenith` @ `76f912fa08`) · `feat/rebrand` (`8c4e083700`, now contained in feat/branding) |
| Plan 01 | ✅ run, tests, upstream merge; `script/bundle-mac -i` → `/Applications/Zenith Dev.app` opens (home machine, 2026-11-16) |
| Icon | ✅ `brand/zenith-icon.svg` (layers `background`/`glyph`) + 512/1024 PNGs; swapped into all 8 `crates/zed/resources/app-icon*.png` on `feat/branding` |
| Plan 02 rebrand | ✅ code done, compiled, tests pass, bundle opens — see §2b |
| Plan 32 welcome | 🟨 `feat/welcome` merged into fork `zenith` (`2800023217`, pushed 2026-11-17; check + welcome/palette tests green). In the home app (`feat/look` @ `65c87e35ba`, installed 2026-11-18 00:05). Owner: visual check, remove README notice |
| Plan 33 accounts | ⬜ brief only; Sign In hidden meanwhile |
| Plan 34 Claude Design | 🟨 fork `feat/look` @ `c52e3978da` pushed — steps 1–4f, 6a, 9a, 10a, 11b (plan 34 §Progress + "Main board check"): built-in look (Archipelago Icons in-app, JetBrains Mono, owner profile defaults), tool-window headers + "···" menu, tab accent line, root location, indent status item, title bar mark + gear, Search Everywhere per board, Recent Files popup, ⌃Tab Switcher, Recent Locations code lines, picker 🔍/esc field, Go to Line dialog. Not merged into `zenith`. **Nothing after `9c2cf04a91` seen in a running app** |
| Plan 21 inspections | 🟨 fork `feat/look` @ `c52e3978da`: on save, changed files, folder, current file, project, PHPCBF fix, suppress (⌘.), settings (plan 21 §Progress); 33 tests. Home app = `9c2cf04a91` (no suppress, no file/project scope) |
| `.zenith` project dir | ✅ `feat/zenith-dir` merged into `zenith` (`0cb9e7432e`). New settings/tasks/debug go to `.zenith/`; `.zed/` still read (settings merged, `.zenith` wins). Not yet checked in running app |
| UI mockups | ✅ `docs/ui-mockups` merged into `main` (`219d2e7`): `mockups/zenith-v1.html` (all features on one screen), `mockups/zenith-v2.html` = target look (Editing / Debugging / Agent review scenes, orange = agents only), Claude Design export (`5e0d712`); default Driftwood + Archipelago Icons (plan 14), being built in plan 34 |
| First build `cargo build -p zed` | ✅ on work machine (debug, after installing the Metal Toolchain; first build ≈ 1 h, incremental ≈ 2 min; target/ ≈ 25 GB) |
| `cargo test -p workspace` | ✅ 307 passed (work machine) |
| Toolchain | Rust 1.98.1 (pinned by repo), Xcode 26.5, cmake 4.5 |

Installed on **work** machine (home ran `zed-kit/install.sh` 2026-11-17: zed-php-fmt link + phpactor.json; WPCS 3.4.1 in global Composer (phpcs pinned to 3.13.6 — WPCS has no PHPCS 4 support; Homebrew phpcs 4.0.4 also present, `~/.zshrc` puts `~/.composer/vendor/bin` first); no Xdebug; home Zed settings = symlink to `~/GithubProjects/zed-config`, Phpactor off via `"!phpactor"` since its first commit): `~/.local/bin/zed-php-fmt` → repo symlink; `~/.config/phpactor/phpactor.json`; Zed settings backups `~/.config/zed/settings.json.backup-20261115-*`.
Machine facts: PHP 8.5, Composer 2.10, Node 22, phpcs + WPCS in `~/.composer/vendor/bin`, Valet, fswatch; no Xdebug, no Intelephense licence. Home machine: Xcode 26.5 + Metal Toolchain, cmake.

Open issues (plan 03):

- Verify 03 in Zed: go-to-def/rename, Phpactor code action, PHPCS (WP) / PHPStan (Laravel) inline, Pint on save, no duplicate completions, per-project Intelephense stubs applied, Phpactor auto-download.
- Xdebug not loaded (`install.sh --with-xdebug` or Herd/Valet PHP).
- `install.sh --dry-run` labels real checks as `dry` too (cosmetic).

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

0. Build `feat/look` @ `c52e3978da` (only when the owner asks; ≈ 20–50 min, app-build cache kept, 95 GiB free) and visually check everything since `9c2cf04a91` against `mockups/claude-design/` (Main, SearchEverywhere, ToolWindows boards; headless Chrome screenshots of the boards: `--headless=new --screenshot`). Fix what is off. If webrtc download fails, see `docs/guides/fork-findings.md` `LK_CUSTOM_WEBRTC`. App backups: `~/Applications-backup/Zenith Dev-20261118-home.app` (= `65c87e35ba`).
0b. Owner: merge `feat/look` into `zenith` after the visual check; remove the fork README notice.
0c. Next feature after the visual check: plan 27 TODO window (2–3 d, owner leaning there); then plan 21 baseline/new-since-branch, plan 05 Local History. Board gaps waiting on plans: plan 34 "Main board check" table.
0a. Owner to decide: JetBrains settings import first slice (plan 31) on the welcome Customize page — detect `~/Library/Application Support/JetBrains/<Product><ver>`, import keymap base + editor font/size/tabs/soft wrap/theme; hide or redirect "get merch"/"open docs".
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
cd ~/GithubProjects/zenith && claude   # work machine: ~/GithubRepos/zenith
> Read HANDOFF.md, CLAUDE.md and .claude/handoff-169c3411-c7d8-40dd-a660-6141116af62d.md (the current brief). Ask the owner whether to restart the bundle and about §4 steps 0/0b/0c; never rebuild the app unless asked in that message.
```
