# 07 — Test Runner UI

## Goal

JetBrains-style test tool window: tree of suites/tests with pass/fail/skip, durations, failure diff, rerun failed, jump to source, run/debug from gutter.

## Parity checklist

- [ ] Run tests at cursor / file / directory / all (must) — Zed already has gutter runnables + tasks; we add the results UI
- [ ] Results tree with status icons, durations (must)
- [ ] Failure details: message, stack trace with clickable frames, expected/actual diff (must)
- [ ] Rerun failed (must)
- [ ] Rerun single test from tree (must)
- [ ] Debug test (reuse Zed debugger + Xdebug/node adapters) (must)
- [ ] Watch mode / auto-rerun on save (later)
- [ ] History of runs (later)
- [ ] Coverage (out of scope)

## Frameworks (v1)

| Framework | Structured output |
|---|---|
| PHPUnit / Pest | `--log-junit <file>` or `--teamcity` |
| Jest | `--json --outputFile` or custom reporter |
| Vitest | `--reporter=json` / `junit` |
| Playwright | `--reporter=json` (later) |

Prefer **JUnit XML** as the common format (all support it) + TeamCity streaming for PHPUnit for live progress.

## UX

- Bottom dock panel "Tests": toolbar (Rerun, Rerun Failed, Stop, Filter: failed only, Sort), tree, details pane.
- Gutter: after a run, test functions show ✓/✗ marks.
- Clicking failure frame → opens file:line.
- Expected/actual → "Show Diff" opens a diff Item.

## Architecture

- Crate `zenith_test_runner`.
- Run model: `TestRun { id, framework, command, started, status, root: TestNode }`.
- Execution: extend existing task spawn — run command with reporter flags injected + temp report path; stream stdout to terminal as today, parse report on exit (and TeamCity lines live).
- Framework detection per worktree: `vendor/bin/phpunit`, `vendor/bin/pest`, `package.json` devDeps (jest/vitest).
- Location mapping: JUnit `file`/`line` attributes; fallback to symbol search via LSP workspace symbols.
- Rerun failed: build filter args (`--filter 'A::b|C::d'`, jest `-t`, vitest `-t`).
- Docker: command prefix from feature 11 (`docker compose exec app`) + path mapping container→host.

## Settings

```json
"zenith": {
  "test_runner": {
    "enabled": true,
    "frameworks": {
      "phpunit": { "command": "vendor/bin/phpunit", "prefix": null },
      "pest": { "command": "vendor/bin/pest" },
      "jest": { "command": "npx jest" },
      "vitest": { "command": "npx vitest run" }
    },
    "path_mappings": { "/var/www/html": "." }
  }
}
```

## Actions & keymap

`RunTestAtCursor` (ctrl-shift-r), `RerunLast` (cmd-r in panel), `RerunFailed`, `DebugTestAtCursor`, `ToggleTestPanel`.

## Milestones

1. JUnit XML parser + model + unit tests.
2. Panel tree + details + source navigation.
3. PHPUnit/Pest integration incl. TeamCity live progress.
4. Jest/Vitest.
5. Rerun failed/single, gutter marks.
6. Debug test via existing debugger.

## Tests

- Parser fixtures from real PHPUnit/Pest/Jest/Vitest outputs.
- Filter-arg builder per framework.
- gpui panel smoke test.

## Risks

- Pest/PHPUnit version differences in output — fixtures for each major.
- Data-provider tests naming (`test with data set #1`) mapping to source.

## Effort

2–3 weeks.
