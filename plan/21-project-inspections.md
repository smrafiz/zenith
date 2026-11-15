# 21 — Project-wide Inspections & Problems Panel (F3)

## Goal

JetBrains "Inspect Code": run analyzers over the whole project (not just open files), browse/filter results, apply quick fixes, baseline support.

## Parity checklist

- [ ] Run on: project / directory / changed files (git) / current file (must)
- [ ] Analyzers: PHPStan, Psalm (opt), PHPCS (WPCS, PSR-12), PHP-CS-Fixer (dry-run), ESLint, TypeScript `tsc --noEmit`, Stylelint (opt), Rector (dry-run as "suggestions") (must)
- [ ] Problems panel: group by severity / analyzer / file / rule; filter; counts in status bar (must)
- [ ] Click → jump; inline diagnostics in open editors stay in sync (must)
- [ ] Quick fixes: PHPCBF/fixer for file/rule, ESLint `--fix`, Rector apply (preview via 09) (must)
- [ ] Suppress: add `@phpstan-ignore`, `// phpcs:ignore`, `eslint-disable-next-line` (must)
- [ ] Baseline awareness (phpstan-baseline.neon) + "only new problems since branch base" (must — critical for legacy WP code)
- [ ] Run before commit (pre-commit check in git panel) (later)
- [ ] Agent tool: `inspections_run` / `inspections_list` via MCP (06) so agents self-verify (must)

## UX

- Bottom panel "Problems" with toolbar: Scope ▾, Analyzers ▾, Run, Stop, Fix All (scope), Group by ▾.
- Status bar: ✗ errors ⚠ warnings (click → panel).
- Progress per analyzer.

## Architecture

- Crate `zenith_inspections`.
- `Analyzer` trait: `detect(project) -> bool`, `command(scope) -> Command`, `parse(output) -> Vec<Problem>`, `fix(problem|file) -> Option<Command>`.
- Machine formats: PHPStan `--error-format=json`, Psalm `--output-format=json`, PHPCS `--report=json`, ESLint `-f json`, `tsc --pretty false` (regex), Rector `--output-format=json`.
- Runs through `zenith_core::process` (Docker prefix from 11, path mapping).
- Results stored per run (`zenith_core::store`), diffable between runs ("new since last run").
- Publish into Zed diagnostics for open buffers (as a diagnostics source) — *verify* how to push non-LSP diagnostics; fallback: virtual LSP server inside Zenith.
- "Changed files" scope: `git diff --name-only <merge-base>`.

## Settings

```json
"zenith": {
  "inspections": {
    "analyzers": { "phpstan": true, "phpcs": { "standard": "WordPress" }, "eslint": true, "tsc": true, "rector": false },
    "run_on_save": "changed_file",
    "max_parallel": 2
  }
}
```

## Milestones

1. Analyzer trait + PHPStan + PHPCS + panel.
2. ESLint + tsc; diagnostics sync.
3. Quick fixes + suppressions.
4. Changed-files / new-since-base scopes.
5. MCP tools; pre-commit hook.

## Tests

Parser fixtures per analyzer (real outputs); suppression insertion golden tests.

## Risks

Large projects: PHPStan full run slow → default scope "changed files", full run on demand; respect analyzer caches.

## Effort

1–2 weeks.
