# 25 — Laravel Tools (F7)

## Goal

Laravel Idea–level navigation and tooling.

## Parity checklist

- [ ] Artisan panel: all commands (`php artisan list --format=json`), run with args form (must)
- [ ] Routes panel: `php artisan route:list --json` → method, URI, name, action; click → controller method (must)
- [ ] Go-to: `route('name')` → route def; `view('a.b')` → Blade file; `config('x.y')` → config key; `trans('…')`/`__()` → lang key; `env('X')` → `.env` (must)
- [ ] Completion for route names, view names, config keys, translation keys, env keys (must)
- [ ] Blade: `<x-component>` → component class/view; `@include('…')` go-to (must)
- [ ] Eloquent: model attributes/relations completion → via `barryvdh/laravel-ide-helper` generated stubs (03) (must)
- [ ] Migrations panel: status, run/rollback (confirm) (later)
- [ ] Tinker console (REPL in terminal) (must, trivial)
- [ ] Log viewer for `storage/logs/laravel.log` with level filter (later)
- [ ] Sail/Herd/Valet detection → interpreter (11) (must)

## Architecture (extension-first, 16)

- **Use the existing `laravel-official` Zed extension (Official Laravel LSP)** before building anything; `laravel-ls` only for gaps (check first for an existing maintained Laravel LS compatible with Zed; reuse if good):
  - Index: routes (from `route:list --json`, refreshed on routes file save), views (`resources/views/**`), config (parse `config/*.php` arrays via tree-sitter), lang files, `.env`.
  - LSP: definition, completion, hover inside the relevant string literals.
- **`zenith_laravel`** crate: Artisan + Routes (+ Migrations, Logs) panels; commands via `zenith_core::process`.
- IDE helper: action "Generate IDE helpers" runs `php artisan ide-helper:generate && ide-helper:models -N && ide-helper:meta`.

## Milestones

1. Survey existing Laravel LS options.
2. Artisan + Routes panels.
3. LS: views/routes/config go-to + completion.
4. Blade components; translations; env.
5. Migrations + log viewer.

## Effort

2–3 weeks.
