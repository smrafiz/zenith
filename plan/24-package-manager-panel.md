# 24 — Composer & npm Panel (F6)

## Goal

Manage dependencies and scripts without leaving the editor.

## Parity checklist

- [ ] Detect `composer.json`, `package.json` (npm/pnpm/yarn/bun via lockfile) in all worktrees, incl. nested (monorepo) (must)
- [ ] Scripts list → run with one click (output in terminal) (must)
- [ ] Dependencies tree: direct deps, installed vs constraint version (must)
- [ ] Outdated check (`composer outdated --format=json`, `npm outdated --json`) with badges (must)
- [ ] Update one / all (confirm), require/add package with search (packagist / npm registry) (must)
- [ ] Security audit (`composer audit --format=json`, `npm audit --json`) (must)
- [ ] Inline hints in `composer.json`/`package.json`: latest version, vulnerable marker (later)
- [ ] Go to package source (vendor/node_modules) (later)

## UX

Left-stripe panel "Packages": per manifest section → Scripts / Dependencies / Dev / Audit. Row actions. Status bar warning if lockfile out of sync with manifest.

## Architecture

- Crate `zenith_packages`; all commands via `zenith_core::process` (Docker prefix from 11).
- Parse JSON outputs; cache results in store with TTL (outdated/audit are network calls — never on startup, on demand or daily).
- Registry search: Packagist API, npm registry API via Zed `http_client`.
- Mutating commands (require/update/remove) → confirm modal showing exact command.

## Milestones

1. Detection + scripts runner.
2. Deps tree + outdated.
3. Audit.
4. Add/update/remove with search.
5. Manifest inline hints.

## Effort

1 week.
