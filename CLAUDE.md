# Zenith — Project Context for Claude

Zenith = fork of Zed aiming at full PhpStorm/WebStorm parity (classic + agentic PHP/JS/WordPress/Laravel dev) while keeping Zed's speed. Owner builds WordPress themes/plugins (RadiusTheme) and Laravel/Node apps.

## Repo & accounts

- Repo: `wp-sigmadevs/zenith` (public). Local: `~/GithubRepos/zenith` (work) / `~/GithubProjects/zenith` (home; fork at `~/GithubProjects/zed`). Default branch `main`.
- gh accounts on this machine: `smrafiz` (default, write access) and `wp-sigmadevs` (owner). Repo settings/admin tasks: `gh auth switch -u wp-sigmadevs`, then switch back to `smrafiz`.
- Personal-account repo ⇒ collaborators can't get admin; that's fine, owner does admin tasks.
- Enabled: Discussions, private vulnerability reporting, secret scanning + push protection, Dependabot alerts.
- Licence: MIT for this repo. Fork code follows Zed licences (GPL-3.0 editor, AGPL server, Apache GPUI); new `zenith_*` crates GPL-3.0-or-later. Standalone LSes (wp-hooks-ls, etc.) MIT in own repos.
- Never use Zed name/logo for Zenith (trademark).

## Layout

```
plan/        32 plan docs — start at plan/README.md (index, phases, timeline)
zed-kit/     plan 03 config layer for STOCK Zed (works today, no fork)
  bin/zed-php-fmt (+ test-zed-php-fmt.sh)   stdin→file→stdout adapter for pint/phpcbf/php-cs-fixer
  install.sh [--dry-run] [--with-xdebug]    idempotent, never overwrites
  apply-template.sh <wordpress|laravel|node> <dir>
  settings.global.jsonc                      keys to merge into ~/.config/zed/settings.json
  phpactor/phpactor.json                     global Phpactor config (completion off)
  templates/{wordpress,laravel,node}/
.github/     issue templates (feature, bug), PR template
```

GitHub tracking: 31 issues (one per plan doc), 6 milestones (Phase 0–5), labels `layer:*`, `type:*`, `continuous`.

## Conventions

- Commits: conventional (`docs:`, `feat(zed-kit):`, `fix:`, `chore:`) — a hook rejects others.
- Fork naming: crates `zenith_*`, umbrella `zenith`, settings key `"zenith"`, branch `zenith`, data dir `~/.local/share/zenith/`, bundle `Zenith.app`.
- All fork code in new crates; upstream files get one-line hooks only (plan/02). Extension/LS-first where possible (plan/16). Shared infra in `zenith_core` (plan/15).
- Zed internal APIs in plan docs are from memory and marked *verify* — check against current Zed source before implementing.
- Supercharger hook blocks writes under `~/.config/` — give the user the exact edit instead; never work around it.

## Engineers

15 subagents in `.claude/agents/` — roster, routing per phase, setup and sources in `.claude/agents/README.md`. `lead-engineer` plans anything new (crates, upstream hooks, LS-vs-fork); one implementer per planned chunk; `code-reviewer` (+ security/performance/accessibility as relevant) before merge; `debugger` for a red gate. Read-only agents can't write; agents never push. Guard hooks live in `.claude/hooks/` (read-only-bash, guard-push, writer-gate).

## Status (2026-11-17)

| Item | State |
|---|---|
| Plan docs 01–31 | ✅ written |
| Repo setup (README, LICENSE, SECURITY, templates, issues, milestones) | ✅ |
| 03 config layer | 🟨 zed-kit built + installed; user's Zed settings merged (Intelephense + Phpactor, extensions twig/dockerfile/make/http, Tailwind in PHP/Blade, telemetry off). **Not yet verified in running Zed.** |
| Fork (01) | ✅ build/run/tests/upstream-merge/bundle (`Zenith Dev.app` opens). `zenith` @ `0cb9e7432e` = upstream + rebrand + `.zenith` dir, pushed — HANDOFF.md §2b |

Installed on machine: `~/.local/bin/zed-php-fmt` → repo symlink; `~/.config/phpactor/phpactor.json`; Zed settings backups `~/.config/zed/settings.json.backup-20261115-*`.
Machine facts: PHP 8.5, Composer 2.10, Node 22, phpcs + WPCS in `~/.composer/vendor/bin`, Valet, fswatch; no Xdebug, no Intelephense licence. Home machine: Xcode 26.5 + Metal Toolchain, cmake.

| Rebrand (02) | ✅ merged into `zenith` (`76f912fa08`); telemetry/auto-update off; logo + tagline replaced |
| `.zenith` project dir | ✅ `feat/zenith-dir` merged into `zenith` (`0cb9e7432e`), pushed. New settings/tasks/debug go to `.zenith/`; `.zed/` still read (settings merged, `.zenith` wins). Not yet checked in running app |
| Icon | ✅ `brand/` |
| Welcome (32) | 🟨 `feat/welcome` merged into fork `zenith` (`2800023217`, pushed 2026-11-17; check + welcome/palette tests green). Not in installed app (no rebuild). Owner: visual check, remove README notice |
| Accounts (33) | ⬜ brief only; Sign In hidden meanwhile |
| Claude Design (34) | 🟨 fork `feat/look` @ `1ce4504494` pushed: steps 1, 2, 3a, 4a, 4b, 4c, 6a done (table in plan 34 §Progress). Not merged into `zenith`, not in an installed app (no rebuild). Next: 4d All tab |
| UI mockups / default look (14) | ✅ `docs/ui-mockups` merged into `main` (`219d2e7`), pushed: `mockups/zenith-v1.html` (all features on one screen), `mockups/zenith-v2.html` (target: Editing / Debugging / Agent review scenes, orange = agents only), Claude Design export (`5e0d712`). Default look decided: Driftwood + Archipelago Icons (plan 14); being built in plan 34 |

## Findings worth keeping

- Rebrand choke points: `crates/paths/src/paths.rs` APP_NAME (+ assert in zed main.rs that APP_NAME_LOWERCASE == bin name), `release_channel` display_name/app_id, `client.rs` ZED_URL_SCHEME + open_listener literals, `install_cli_binary.rs` CLI path, auto-update off via build env `ZED_UPDATE_EXPLANATION`, crash upload off when `ZED_MINIDUMP_ENDPOINT` unset, telemetry defaults in `assets/settings/default.json`. Keychain creds keyed by server URL (keep `zed.dev`).
- Fork's own `CLAUDE.md` hard rule: any source edit ⇒ prepend `> [!IMPORTANT]` + review line to README.md; only the human removes it.
- Release builds: `script/bundle-mac -i` (dev channel → `Zenith Dev.app`); `-d` debug. Unsigned → ad-hoc codesign, universal links off. `-i` exits 1 *after* "Installed application bundle" (upstream script then mv-s the moved app for the DMG) — app is fine. Build regenerates `assets/licenses.md` (stays clean).
- Rebrand keep-as-"Zed" list (services, User-Agent, MCP/DAP client names, fonts/icons/themes, base keymap "Zed", internal `zed:///` mention + `zed://schemas/` URIs, Windows-only names): HANDOFF.md §2b. Logo = contents of `assets/images/zed_logo.svg` + `zed_x_copilot.svg` (no code hook).
- Timings (home, first run): `cargo check -p zed` 11m 13s; bundle zed binaries 11m 10s + remote_server 7m 49s. Plan 17 targets these.
- gpui tests: `cx.update_global::<T, _>` needs `use gpui::BorrowAppContext as _`.
- Welcome screen (plan 32): `workspace::welcome::WelcomeOverride` global (fn ptr → `Option<AnyView>`) replaces upstream page; `zenith::show_onboarding_view` swaps onboarding in `main.rs`/`open_listener.rs`. Tests need `editor::init`, `LoadThemes::All(Box::new(assets::Assets))`, `Client` + `Fs` globals, and `AppState::test` *before* re-init (it resets themes). Never `read` the Workspace inside its own update — read `fs` in the spawned task.
- No-Zed-branding rule (owner, 2026-11-16): nothing user-visible says "Zed". Cheapest levers: `command_palette::humanize_action_name` shows `zed::` as `zenith:` (display only; ids stay `zed::` so keymaps work; also feeds which-key); `title_bar.show_sign_in` default false; own copies in `zenith_welcome` instead of upstream edits. Still Zed-pointing: "zenith: get merch", "zenith: open docs" (zed.dev).
- `ui::Button::full_width()` centers its label; for left-aligned nav drop it and let the column stretch.
- New `IconName` variant needs `assets/icons/<snake>.svg`; `icons` tests fail on a missing or dangling svg.
- Disk/time (work machine, 2026-11-16): `target/` reached 73–80 GiB; `cargo clean` freed 80.1 GiB. Full release bundle from clean 115m 11s; full `./script/clippy` after it 8m 45s; incremental bundle after small UI edits ≈ 51m (35m + 16m). Never `cargo clean`/delete `target/` while a build or clippy runs — it killed clippy (`os error 2`).
- Plinth (`~/GithubRepos/plinth`, Next.js + Prisma + better-auth multi-tenant CMS) fits the Zenith website (`zenith.plinthsites.com`), not accounts: users are CMS editors, no blob/licence/registry (plan 33).

- Title bar (plan 34): upstream holds sections in `ArrayVec<_, 5>` (`crates/title_bar/src/title_bar.rs` ~257); a 6th push panics `CapacityError` when the onboarding banner shows. Add Zenith UI as ONE section (`zenith_title_bar::middle`).
- Zenith keymap: `assets/keymaps/zenith.json` loads after the base keymap (`zed.rs` `load_default_keymap`, `settings::ZENITH_KEYMAP_PATH`), so it wins over JetBrains bindings. Loading `.unwrap()`s: every action named there must be linked into the app, and a test that loads it must link the action's crate (`KeymapFile::load_asset` fails on unknown actions). `"secondary-…"` = cmd on macOS, ctrl elsewhere. Don't edit upstream default keymaps.
- Optional actions without a crate dependency: `cx.build_action("debugger::Start", None).ok()`.
- Changing `assets/settings/default.json` breaks upstream tests that assume the old default; pin the old value inside those tests (done for project_panel `test_focus_follows_mouse_into_blank_area`, git_ui `test_history_tab_pane_navigation_focuses_rendered_panel`). Run the touched crates' tests after any default change.
- Picker: `render_header` draws only when there are matches, below the query editor. For chrome above the search box wrap the picker and build it with `.embedded()`; the wrapper is the `ModalView`.
- Upstream file edits that can't be one line: append a block at end of file (e.g. `command_palette.rs` shared-history fns) — modified upstream lines conflict on sync, an appended block rarely does.
- Disk (work machine, 2026-11-17): `cargo test -p zed` ≈ +18 GiB; `target/debug/incremental` grows to ≈ 26 GiB (`rm -r` is safe when nothing builds); `./script/clippy` builds the release profile. After big test runs `cargo clean -p <crates>`. Keep ≥ 30 GiB free.
- PHP symbol kinds (checked 2026-11-17 via workspace/symbol): Intelephense 1.18.5 trait = Module(2); PHPantom 0.11.1 trait = Class(5), names namespaced (`App\ZenTrait`); Intelephense + PHPantom: class 5, interface 11, enum 10, function 12. Phpactor 2026.10.07.0: class/interface/trait/enum all Class(5), namespaced, plus PHP stub symbols (zend_*) in results. Phpactor phar at `~/.local/bin/phpactor` (runs on PHP 8.5). Zed's PHP extension installs both under `~/Library/Application Support/Zed/extensions/work/php/`.
- Flaky upstream test: `agent_ui` `test_migrate_thread_remote_connections_backfills_from_workspace_db` failed once under parallel load, passed 5 reruns. Suspect the shared test KVP DB; not ours.
- Zed PHP extension: Phpactor is the default LS; Intelephense alternate; licence via `~/intelephense/licence.txt` or `lsp.intelephense.initialization_options.licenceKey`. Xdebug debug adapter built into the PHP extension.
- Zed extensions exist: `laravel-official` (Official Laravel LSP — plan 25 builds on it), `laravel` (community), `http` (.http highlighting only), `twig`, `codebook`, `harper`. No PHPStan/WordPress extension.
- Intelephense `stubs` setting replaces defaults — templates list defaults + `wordpress`.
- phpcbf exit codes: 0 none, 1 fixed, 2 fixed+remaining, 3 error (wrapper treats ≤2 as success).

- `.zenith` project dir (fork `823272e9d0`): choke point `crates/paths/src/paths.rs` (`local_settings_folder_name` = `.zenith`; `legacy_*` = `.zed`; `is_local_settings_folder_name`). Settings for both folders share one key (parent dir) in `SettingsStore`, so `project_settings.rs::load_merged_local_settings` loads both and merges (`util::merge_json_value_into`, `.zenith` wins). Tasks/debug key by the folder itself ⇒ both listed. Other touch points: worktree always-scan, `agent/src/tools/tool_permissions.rs::is_local_settings_component` (security: both folders prompt), task_inventory `.vscode` hiding, debugger new_process_modal, json_schema_store, security/alert modal text. ~10 upstream files — expect merge conflicts there.
- Agent sensitive-path tests (`edit_file_tool.rs` `expect_authorization().await`) **hang forever** instead of failing when the prompt doesn't fire — kill after a few minutes, a hang = fail.
- Disk (home, 2026-11-16): target/ grew 93 → ~120 GiB from one session of per-crate `cargo test` + clippy + one release bundle; disk hit 0 mid-run (ENOSPC breaks Bash/Edit entirely). `cargo clean` freed 135.8 GiB. Check `df -h ~` before test/bundle runs; keep ≥ 30 GiB.
- Look sources live outside this repo: `~/GithubProjects/archipelago` (Driftwood theme + Archipelago Icons = Atom Material, MIT) and `~/GithubProjects/zed-config` (owner's default profile). Islands geometry (rounded, gapped docks) can't be a Zed theme — needs `workspace` dock rendering (plan 14 risk). Zed icon themes match exact names/suffixes only (`blade.php`, `test.ts` ok; `*Test.php`, `*Controller.php` impossible).
- Mockup checks: headless Chrome (`--headless=new --screenshot` / `--dump-dom`) has a 500 px minimum window; click-test by injecting a script that clicks, then `--dump-dom` and grep PASS/FAIL. Repo mockups are full HTML docs; artifact copies omit doctype/head (the Artifact tool adds them).
- Per-crate gates are cheap after a warm build: `cargo check` 8 crates ≈ 52 s; `cargo test -p project --test integration <filter>` ≈ 1 min; incremental release bundle 12 min.

## Open issues

- Verify 03 in Zed: go-to-def/rename, Phpactor code action, PHPCS (WP) / PHPStan (Laravel) inline, Pint on save, no duplicate completions, per-project Intelephense stubs applied, Phpactor auto-download.
- Xdebug not loaded (`install.sh --with-xdebug` or Herd/Valet PHP).
- `install.sh --dry-run` labels real checks as `dry` too (cosmetic).

## Next steps

1. User restarts Zed, applies a template to a real WP/Laravel project, runs `zed-kit/README.md` checklist → fix failures → mark 03 ✅ in plan/README.md and close its issue.
2. User clears disk + installs Xcode + `brew install cmake`.
3. Fork `zed-industries/zed` → `wp-sigmadevs/zed`, clone to `~/GithubRepos/zed`, branch `zenith`, `cargo run` (plan 01), then 17 → 15 → 18 → Phase 1 (04 scratches, 14 toolbar, 05 local history…).
