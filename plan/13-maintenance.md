# 13 — Maintenance: Upstream Sync, Release, QA

## Upstream sync

- Cadence: weekly (Zed ships weekly). Small merges beat big ones.
- Procedure:
  ```sh
  git fetch upstream
  git checkout main && git merge --ff-only upstream/main && git push
  git checkout zenith && git merge main
  cargo build && cargo test -p zenith -p zenith_*   # all zenith crates
  ```
- Merge, don't rebase `zenith` (shared history, fewer repeated conflict resolutions).
- Every clone that merges upstream runs once: `git config rerere.enabled true && git config rerere.autoupdate true` (local setting, not pushed; enabled in the main clone 2026-11-17). Resolutions live in `.git/rr-cache`, so a fresh clone starts with none.
- Track time per merge in a log (`plan/sync-log.md`) → kill criteria in README.
- Each upstream release: scan changelog for features overlapping ours → drop ours if equivalent.

## Release (personal use)

- Build: release bundle script → copy `.app` to `/Applications/Zenith.app`.
- Distinct bundle id/name so it coexists with stable Zed (*verify how dev/preview channels set this*).
- Disable/redirect auto-update to avoid being replaced by upstream builds.
- Tag `zenith-vYYYY.MM.DD`.

## CI (optional, GitHub Actions on fork)

- On push to `zenith`: `cargo check`, `cargo test -p zenith_*`, clippy on zenith crates.
- Weekly scheduled job: test-merge `upstream/main` into `zenith`, open an issue on conflict.
- macOS runners are expensive — run the full build locally; CI only checks zenith crates.

## QA checklist (per release)

- [ ] Open Laravel project, WP plugin, TS project.
- [ ] LSP: completion, go-to-def, rename, diagnostics.
- [ ] Each zenith feature smoke test (scratch run, history revert, IDE server `/ide` from Claude Code, test run, HTTP request, refactor preview, merge view, compose exec, DB query).
- [ ] Agent Panel + Claude Code via ACP still work.
- [ ] No settings migration errors on startup.

## Docs

- Each feature doc gets an "Implemented" section: crate, settings, known gaps.
- `zed-kit/README.md` explains install + config for a fresh machine.
