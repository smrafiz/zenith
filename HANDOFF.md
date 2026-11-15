# Zenith — Handoff (work machine → home machine)

Last updated: 2026-11-15. Read with `CLAUDE.md` (project rules) and `plan/README.md` (roadmap).

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
git -C zed fetch origin && git -C zed switch zenith 2>/dev/null || git -C zed switch -c zenith

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
| Fork | ✅ `wp-sigmadevs/zed` (smrafiz has write), branch `zenith` **local only, not pushed yet** |
| First build `cargo build -p zed` | ✅ on work machine (debug, after installing the Metal Toolchain; first build ≈ 1 h, incremental ≈ 2 min; target/ ≈ 25 GB) |
| Toolchain | Rust 1.98.1 (pinned by repo), Xcode 26.5, cmake 4.5 |

## 3. Open decisions (owner)

1. Commit prefix in the fork: `feat(<crate>):` (recommended, passes the commit hook) or `zenith(<feature>):` (plans 02/16 say this; the hook rejects it). Then have docs-editor fix plans 02/16.
2. Keep or drop the `<example>` block in agent descriptions (Anthropic's guidance dropped them in Apr 2026).
3. "scratch removed": unclear whether this meant dropping the Scratch files feature (plan 04). Confirm.
4. Plan 22 scope: Zed now isolates agent threads in worktrees upstream. Have lead-engineer shrink plan 22 to the gaps.

## 4. Next steps (in order)

1. Home: `cd ~/GithubRepos/zed && cargo build -p zed` → `cargo run` launches a dev window → `cargo test -p workspace` (plan 01 "Done when").
2. `git -C ~/GithubRepos/zed push -u origin zenith` once it builds.
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
> Read HANDOFF.md and CLAUDE.md. Continue from "Next steps" step 1: build the fork at ~/GithubRepos/zed and verify plan 01.
```
