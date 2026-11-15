# 01 — Prerequisites & Fork Setup

## Current machine state (checked 2026-11-15)

| Need | State | Action |
|---|---|---|
| Rust toolchain | ✅ rustup + cargo | `rustup update` (repo pins version via `rust-toolchain.toml`) |
| Full Xcode | ❌ only Command Line Tools | Install from App Store, then `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer` and `sudo xcodebuild -license accept` |
| cmake | ❌ | `brew install cmake` |
| Free disk | ❌ 23 GB (95% used) | Free to **≥ 80 GB** (Xcode ~15–40 GB, `target/` 30–60 GB) |
| Existing clone | none | — |

Disk cleanup candidates: `~/Library/Developer/Xcode/DerivedData`, `~/Library/Caches`, old `node_modules` (`npx npkill`), `~/.cargo/registry` cache, Docker images (`docker system prune` — confirm first, destructive).

## Fork setup

1. Fork `zed-industries/zed` on GitHub → `<you>/zed`.
2. Clone:
   ```sh
   git clone git@github.com:<you>/zed.git ~/GithubRepos/zed
   cd ~/GithubRepos/zed
   git remote add upstream https://github.com/zed-industries/zed.git
   ```
3. Branches:
   - `main` — mirrors `upstream/main`, never commit here.
   - `zenith` — integration branch = main + all zenith features.
   - `feat/<name>` — one per feature, branched from `zenith`.
4. Run `script/bootstrap` if present (*verify*) — reports missing deps.

## Build & dev loop

| Task | Command |
|---|---|
| Debug run | `cargo run` |
| Faster incremental | set `[profile.dev] debug = "line-tables-only"` locally only if the repo doesn't already |
| Single crate tests | `cargo test -p <crate>` |
| Release bundle | `script/bundle-mac` (*verify name/flags*) → `.app` in `target/` |
| Lint | `cargo clippy -p <crate>` / repo's `script/clippy` |

Expected: first build 30–60 min, incremental 30 s–3 min.

## Running beside stock Zed

- Dev builds use a separate channel/data dir ("Zed Dev") — your stable Zed settings stay untouched (*verify*).
- Keep stable Zed installed as fallback until feature 05 is stable.
- Copy settings: `cp ~/.config/zed/settings.json` → dev channel config dir if it differs.

## Done when

- [x] `cargo run` launches a dev Zed window.
- [x] `cargo test -p workspace` passes.
- [ ] Release bundle builds and opens from `/Applications`.
- [x] `git fetch upstream && git merge upstream/main` into `zenith` works.
