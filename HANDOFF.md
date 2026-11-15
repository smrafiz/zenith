# Zenith — Handoff (work machine → home machine)

Last updated: 2026-11-15 (evening, work machine). Read with `CLAUDE.md` (project rules) and `plan/README.md` (roadmap).

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
| Fork | ✅ `wp-sigmadevs/zed` (smrafiz has write). Branches: `zenith` (`596dfdcf32` = upstream main) · `feat/branding` (`09d5ede914`: icon + bundle names/ids) · `feat/rebrand` (`04f99cf8a4`, from feat/branding: core rebrand + WIP strings) |
| Plan 01 | 🟨 run ✅, `cargo test -p workspace` ✅ (307), upstream merge ✅; release bundle (`script/bundle-mac -i`) was building when I left — result unknown |
| Icon | ✅ `brand/zenith-icon.svg` (layers `background`/`glyph`) + 512/1024 PNGs; swapped into all 8 `crates/zed/resources/app-icon*.png` on `feat/branding` |
| Plan 02 rebrand | 🟨 see §2b |
| First build `cargo build -p zed` | ✅ on work machine (debug, after installing the Metal Toolchain; first build ≈ 1 h, incremental ≈ 2 min; target/ ≈ 25 GB) |
| `cargo test -p workspace` | ✅ 307 passed (work machine) |
| Toolchain | Rust 1.98.1 (pinned by repo), Xcode 26.5, cmake 4.5 |

## 2b. Rebrand (plan 02) — status

Owner decisions: **full rebrand** ("everything"), **telemetry/crash/auto-update off**, settings **copied once** (done).

`feat/rebrand` commits:
- `9359dfe882` core (complete, uncompiled): `paths.rs` APP_NAME "Zenith" (+ removed main.rs bin-name assert), release_channel display_name + app_id → `io.github.wp-sigmadevs.Zenith*`, URL scheme `zenith://` / `zenith-cli://` (+ Cargo.toml osx_url_schemes), CLI → `/usr/local/bin/zenith`, auto-update off via `.cargo/config.toml` `ZED_UPDATE_EXPLANATION`, telemetry defaults off, DMG `Zenith-<arch>.dmg`, plist strings.
- `04f99cf8a4` **WIP, unfinished, uncompiled**: ~151 lines in 65 files of user-visible "Zed" → "Zenith" (agent was stopped mid-way, last step "scheme seds"). Rule: app/editor → Zenith; Zed's services/company (zed.dev account, Zed AI/Pro, billing, extension registry, Zed Industries) stay "Zed". Keep identifiers, `ZED_*` env, `.zed/` project dir, `.zed_server`, zed.dev URLs, licences, docs/.

To finish:
1. Review `git -C ../zed diff feat/branding..feat/rebrand` — esp. the WIP commit for over-replacement (service refs) and half-done scheme edits.
2. Finish the remaining strings: `git grep -n '"[^"]*\bZed\b' -- 'crates/*.rs'`, apply the rule above.
3. `cargo check -p zed` → `cargo test -p zed -p release_channel -p paths -p cli` → fix tests asserting old text/URLs.
4. Merge into `feat/branding`, `script/bundle-mac -i` → `/Applications/Zenith Dev.app` opens with Zenith icon/name, reads `~/.config/zenith`.
5. Fix `plan/README.md` line 3 (says bundle id `dev.zenith.app`; actual `io.github.wp-sigmadevs.Zenith`).
6. Fork README.md has the required `> [!IMPORTANT]` 2-line notice (fork CLAUDE.md hard rule) — owner removes it by hand before merging into `zenith`.

Data: `~/.config/zenith` and `~/Library/Application Support/Zenith` were copied from Zed on the work machine (db via `sqlite3 .backup`, integrity ok). At home, repeat: `cp -Rn ~/.config/zed/ ~/.config/zenith/` and the sqlite `.backup` loop for `db/*/db.sqlite`.

Name risk: pending USPTO "ZENITH" word mark (Zenith IOS Manager LLC, filed Jun 2025) — goods/services unchecked. Check before any public release.

## 3. Open decisions (owner)

1. Commit prefix in the fork: `feat(<crate>):` (recommended, passes the commit hook) or `zenith(<feature>):` (plans 02/16 say this; the hook rejects it). Then have docs-editor fix plans 02/16.
2. Keep or drop the `<example>` block in agent descriptions (Anthropic's guidance dropped them in Apr 2026).
3. "scratch removed": unclear whether this meant dropping the Scratch files feature (plan 04). Confirm.
4. Plan 22 scope: Zed now isolates agent threads in worktrees upstream. Have lead-engineer shrink plan 22 to the gaps.

## 4. Next steps (in order)

1. Finish the rebrand (§2b steps 1–6); this also closes plan 01's last item (bundle opens from `/Applications`).
2. Merge `feat/branding` → `zenith` after review.
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
