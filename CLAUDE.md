# Zenith — Project Context for Claude

Zenith = fork of Zed aiming at full PhpStorm/WebStorm parity (classic + agentic PHP/JS/WordPress/Laravel dev) while keeping Zed's speed. Owner builds WordPress themes/plugins (RadiusTheme) and Laravel/Node apps.

## Repo & accounts

- Repo: `wp-sigmadevs/zenith` (public). Local: `~/GithubRepos/zenith`. Default branch `main`.
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

## Status (2026-11-15)

| Item | State |
|---|---|
| Plan docs 01–31 | ✅ written |
| Repo setup (README, LICENSE, SECURITY, templates, issues, milestones) | ✅ |
| 03 config layer | 🟨 zed-kit built + installed; user's Zed settings merged (Intelephense + Phpactor, extensions twig/dockerfile/make/http, Tailwind in PHP/Blade, telemetry off). **Not yet verified in running Zed.** |
| Fork (01) | 🟨 `wp-sigmadevs/zed` forked (smrafiz write), cloned to `~/GithubRepos/zed`, branch `zenith` pushed; debug build ✅, `cargo test -p workspace` ✅ (307); `cargo run` ✅; release bundle pending — see HANDOFF.md |

Installed on machine: `~/.local/bin/zed-php-fmt` → repo symlink; `~/.config/phpactor/phpactor.json`; Zed settings backups `~/.config/zed/settings.json.backup-20261115-*`.
Machine facts: PHP 8.5, Composer 2.10, Node 22, phpcs + WPCS in `~/.composer/vendor/bin`, Valet, fswatch; no Xdebug, no Intelephense licence, no cmake.

## Findings worth keeping

- Zed PHP extension: Phpactor is the default LS; Intelephense alternate; licence via `~/intelephense/licence.txt` or `lsp.intelephense.initialization_options.licenceKey`. Xdebug debug adapter built into the PHP extension.
- Zed extensions exist: `laravel-official` (Official Laravel LSP — plan 25 builds on it), `laravel` (community), `http` (.http highlighting only), `twig`, `codebook`, `harper`. No PHPStan/WordPress extension.
- Intelephense `stubs` setting replaces defaults — templates list defaults + `wordpress`.
- phpcbf exit codes: 0 none, 1 fixed, 2 fixed+remaining, 3 error (wrapper treats ≤2 as success).

## Open issues

- Verify 03 in Zed: go-to-def/rename, Phpactor code action, PHPCS (WP) / PHPStan (Laravel) inline, Pint on save, no duplicate completions, per-project Intelephense stubs applied, Phpactor auto-download.
- Xdebug not loaded (`install.sh --with-xdebug` or Herd/Valet PHP).
- `install.sh --dry-run` labels real checks as `dry` too (cosmetic).

## Next steps

1. User restarts Zed, applies a template to a real WP/Laravel project, runs `zed-kit/README.md` checklist → fix failures → mark 03 ✅ in plan/README.md and close its issue.
2. User clears disk + installs Xcode + `brew install cmake`.
3. Fork `zed-industries/zed` → `wp-sigmadevs/zed`, clone to `~/GithubRepos/zed`, branch `zenith`, `cargo run` (plan 01), then 17 → 15 → 18 → Phase 1 (04 scratches, 14 toolbar, 05 local history…).
