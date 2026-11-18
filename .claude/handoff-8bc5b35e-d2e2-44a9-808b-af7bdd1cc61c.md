## Handoff — Zenith (plan 21 inspections) — 2026-11-18

### Done
- Plan 21 M1a, M1b-1, M1b-2a, M1b-2b, M3a in new crate `crates/zenith_inspections` (fork `feat/look`, pushed through `9c2cf04a91`). Commit list + notes: `plan/21-project-inspections.md` §Progress (zenith `main`, pushed through `95d3bd2`).
  - PHPCS/PHPStan on save → editor diagnostics; "inspect changed files" (git); "fix file with PHPCBF"; `zenith.inspections` settings; project panel folder → **Inspect PHP Files**.
- Two independent reviews; all MUST/SHOULD findings fixed (`0de1f893e7`, `9efcff7fff`, `b362cc109d`). 25 crate tests, each regression test proven by mutation.
- Engineering notes added to `CLAUDE.md` §Findings (moved 2026-11-18 to `docs/guides/fork-findings.md`) (diagnostics push path + test-support trap, ignored-folder scan, deps, PHPCS columns, bundle cost). Committed + pushed (`146d106`).

### In Flight
- none. Session ran on the **work** machine (`~/GithubRepos/`). Its release bundle (started 17:16) was killed by the shutdown; work app = 2026-11-16 build, backup `~/Applications-backup/Zenith Dev-20261118-1716.app`.
- Home machine (`~/GithubProjects/`, checked 2026-11-18): zenith `main` and fork `feat/look` @ `9c2cf04a91` in sync with origin; installed app = `feat/look` @ `65c87e35ba` (2026-11-18 00:05), so no plan-21 feature on either machine yet; 114 GiB free.

### Decisions Made
- Diagnostics via `LspStore::merge_lsp_diagnostics` + reserved server ids, no virtual LSP: works with no running server; `update_diagnostic_entries` is test-only.
- Columns: map PHPCS tab-expanded columns back to UTF-16 instead of `--tab-width=0`: 0 changes which sniffs fire.
- PHPStan runs only with a project config: without one it is noisy on WordPress.
- A tool that did not run clears its old findings; a failed run keeps them and shows the failure once (re-shown after a later success).
- Folder action lives in `zed_actions::zenith_inspections::InspectFolder`; upstream `project_panel.rs` gets a 6-line menu entry (exception to "append only": placed beside "Find in Folder…").
- Owner approved deleting `target/debug/incremental` (10 GiB) mid-build.

### What Failed
- `git checkout -- <file>` to undo a mutation: wiped uncommitted fixes once. Use a cp backup.
- First "ignored files" test: passed with the fix removed (Zed doesn't scan ignored folders). Replaced with an ignored file in a scanned folder.
- A Python patch replaced a span too wide and deleted `notify`/`fix_current_file`; restored from `git show HEAD:`.

### Blockers
- App not seen running with any plan-21 feature: needs the bundle to finish (≈1 h+ on next start).

### Worktrees
- none (main checkouts only: `~/GithubRepos/zed` `feat/look`, `~/GithubRepos/zenith` `main`).

### Files Touched
- `crates/zenith_inspections/**` (new crate), `crates/zenith_php_tools/src/zenith_php_tools.rs` (`worktree_trusted`, `environment` pub), `crates/settings_content/src/zenith.rs` + `assets/settings/default.json` (`zenith.inspections`), `crates/zenith/**` (`inspections` feature), `crates/zed_actions/src/lib.rs` (appended module), `crates/project_panel/src/project_panel.rs` (menu entry), root `Cargo.toml`/`Cargo.lock`.
- zenith: `plan/21-project-inspections.md`, `plan/README.md`, `CLAUDE.md`, `HANDOFF.md`.

### Resume With
Read zenith `CLAUDE.md`, `HANDOFF.md` and this brief. Ask the owner whether to restart `./script/bundle-mac -i` (≈1 h, check `df -h` ≥30 GiB first), then visually check plan-21 features on a real WordPress project; next plan-21 step is suppress actions (`// phpcs:ignore`, `@phpstan-ignore`).

### Start With
none

### Measurements
- Free disk during release bundle: 39 GiB at 17:16 → 25 GiB at 17:42 (1 093 crates by 17:54); +8 GiB after deleting `target/debug/incremental` (10 GiB on disk).
- rustc `--crate-name project` (release) elapsed 52:45 at 18:23 and still running.
- PHPCS PSR12 on `\t$x=1;`: no flag → col 7; `--tab-width=4` → col 7; `--tab-width=0` → col 4 plus extra `ScopeIndent.Incorrect` (WPCS 3.4.1, `~/.composer/vendor/bin/phpcs`).
- `zenith_inspections` tests: 25 passed (`cargo test -q -p zenith_inspections`, 2026-11-18 ≈18:00).

### Rejected — do not rebuild
- `update_diagnostic_entries`: compiled only with `project/test-support`; app build fails (shipped by mistake 1ade746a4a..0de1f893e7, fixed 9efcff7fff).
- PHPCS `--tab-width=0`: changes which sniffs fire (measurement above).
- Mutating `PATH` in tests (`set_var`): races with parallel tests running scripts; replaced by `ToolEnvironment` global.
- Global per-path `Running` map: a save in window B cancelled window A's run; now keyed by project entity id and self-removing.

### Dead ends
- Reviewer's claim "PSR12 default tab width may be 0": measured false (see Measurements).

### Open questions
- Unverified: whether PHPStan reports unmatched ignore patterns on a single-file run (code now handles it either way).
- Unverified: collab guests receiving summaries for the reserved server ids.
- Untested: per-project `Running` tracking, PHPCBF using `ToolEnvironment`, the folder menu entry/selection, git failure in one folder hidden when another has files (known gap), no cancel for big folder runs.

### Reproduce
- `cd ~/GithubRepos/zed && set -o pipefail; cargo test -q -p zenith_inspections` (25 pass); `./script/clippy -p zenith_inspections`; `cargo check -p zenith` (must be 0 errors without test-support).
- Mutation proof: `cp file backup; perl -0pi -e 's/…/…/' file; cargo test …; cp backup file; re-run suite`.
- Bundle: `df -h ~` ≥30 GiB, then `./script/bundle-mac -i` (log to scratchpad); installs `/Applications/Zenith Dev.app` (exits 1 after "Installed application bundle", normal).
