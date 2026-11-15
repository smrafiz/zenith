# Zenith — Master Plan (Zed fork with JetBrains parity)

**Zenith** = fork of Zed. Bundle: `Zenith.app`, id `io.github.wp-sigmadevs.Zenith` (Dev: `…Zenith-Dev`), settings key `"zenith"`, crates `zenith_*`, branch `zenith`. Never ship with Zed name/logo (trademark); keep GPL/AGPL licence + publish source if distributed.

Goal: make Zed a full replacement for PhpStorm/WebStorm for classic **and** agentic PHP/JS development, by (a) configuring stock Zed + extensions where possible and (b) maintaining a fork of Zed for features that need core changes.

> Status legend: ⬜ not started · 🟨 in progress · ✅ done
> Effort figures are estimates for one developer + Claude; revise after the first core feature ships.
> Internal Zed APIs named in these docs (crate names, traits, events) are from memory — **verify against current `main` before implementing** (marked *verify*).

## Documents

| # | File | Layer | Effort | Status |
|---|---|---|---|---|
| 01 | [Prerequisites & fork setup](01-prerequisites.md) | Machine | 1 day | ✅ |
| 02 | [Fork architecture & conventions](02-fork-architecture.md) | Core | — | 🟨 |
| 03 | [Config layer: PHP/JS intelligence, inspections, frameworks](03-config-layer.md) | Config/Extension | 1–3 wk | 🟨 |
| 04 | [Scratch files](04-scratches.md) | Core | ~1 wk | ⬜ |
| 05 | [Local history](05-local-history.md) | Core | 1–2 wk | ⬜ |
| 06 | [Zed as MCP/IDE server for external agents](06-ide-mcp-server.md) | Core | 2–3 wk | ⬜ |
| 07 | [Test runner UI](07-test-runner.md) | Core | 2–3 wk | ⬜ |
| 08 | [HTTP client](08-http-client.md) | Core | 3–4 wk | ⬜ |
| 09 | [Advanced refactoring](09-refactoring.md) | Extension + Core | 4–6 wk | ⬜ |
| 10 | [Git: merge conflicts & interactive rebase](10-git-merge-rebase.md) | Core | 3–4 wk | ⬜ |
| 11 | [Docker / remote interpreters](11-docker-interpreters.md) | Core | 4+ wk | ⬜ |
| 12 | [Database tool](12-database-tool.md) | Core | 2–3 mo | ⬜ |
| 13 | [Maintenance: upstream sync, release, QA](13-maintenance.md) | Process | ongoing | ⬜ |
| 14 | [UI: PhpStorm-style toolbar & interface](14-ui-toolbar.md) | Core | 2–3 wk | ⬜ |
| 15 | [`zenith_core` shared infrastructure](15-zenith-core.md) | Core | 1 wk + | ⬜ |
| 16 | [Upstream contributions & extension-first](16-upstream-and-extensions.md) | Process | ongoing | ⬜ |
| 17 | [Build optimization & Cargo features](17-build-optimization.md) | Dev | 1–2 d | ⬜ |
| 18 | [Performance guard, LS tuning, telemetry](18-performance-and-telemetry.md) | Core/Config | ~2 wk | ⬜ |
| 19 | [WordPress tools](19-wordpress-tools.md) | LS + Core | 2–3 wk | ⬜ |
| 20 | [File & project templates](20-file-templates.md) | Core | 1 wk | ⬜ |
| 21 | [Project-wide inspections & Problems panel](21-project-inspections.md) | Core | 1–2 wk | ⬜ |
| 22 | [Agent worktree manager](22-agent-worktrees.md) | Core | 2–3 wk | ⬜ |
| 23 | [Agent review queue](23-agent-review-queue.md) | Core | 1–2 wk | ⬜ |
| 24 | [Composer & npm panel](24-package-manager-panel.md) | Core | 1 wk | ⬜ |
| 25 | [Laravel tools](25-laravel-tools.md) | LS + Core | 2–3 wk | ⬜ |
| 26 | [Live templates & postfix completion](26-live-templates-postfix.md) | LS | 1–2 wk | ⬜ |
| 27 | [TODO panel](27-todo-panel.md) | Core | 2–3 d | ⬜ |
| 28 | [Bookmarks](28-bookmarks.md) | Core | 3–4 d | ⬜ |
| 29 | [Zenith settings UI](29-settings-ui.md) | Core | 1–2 wk | ⬜ |
| 30 | [Xdebug profiler & code coverage](30-profiler-coverage.md) | Core | 3–4 wk | ⬜ |
| 31 | [PhpStorm/WebStorm migration tool](31-phpstorm-migration.md) | Core/CLI | 1–2 wk | ⬜ |

## Build order & rationale

```
Phase 0  Foundation   01 → 02 → 17 → 15 ; 03 + 18(A7 LS tuning) in parallel (no fork needed)
Phase 1  Quick wins   04 → 14 → 05 → 20 → 27 → 28
Phase 2  Agentic      06 → 23 → 22
Phase 3  Daily depth  21 → 07 → 19 → 08 → 24
Phase 4  Heavy        09 → 10 → 11 → 25 → 26
Phase 5  Big/polish   12 → 29 → 31 → 30
Continuous            13 (maintenance), 16 (upstream PRs), 18 (A6 perf guard)
```

- **Phase 0**: shared core + fast builds before any feature; 03 gives immediate value on stock Zed.
- **Phase 1**: small panels prove fork workflow + measure merge cost (kill criteria). 14 early = entry points for later panels.
- **Phase 2**: agent safety (history → review queue → parallel worktrees) — biggest agentic multiplier.
- **Phase 3**: daily PHP/WP/JS depth.
- **Phase 4–5**: largest, most coupled features; start only once merge cost is known.
- LS-based parts (19, 25, 26, 27 highlight) follow 16's extension-first rule → usable in stock Zed too.

## Timeline (rough, 1 dev + Claude)

| Month | Deliverables |
|---|---|
| 1 | 01, 02, 17, 15, 03, 18-A7, 04 |
| 2 | 14, 05, 20, 27, 28 |
| 3 | 06, 23, 22 |
| 4 | 21, 07, 19 |
| 5 | 08, 24, start 09 |
| 6 | 09, 10 |
| 7 | 11, 25 |
| 8 | 26, start 12 |
| 9–10 | 12 |
| 11 | 29, 31, 30 |

≈ 11 months total. Re-plan after Phase 1 using measured velocity.

## Kill criteria (re-evaluate fork)

Stop and reconsider if any holds after feature 05:
- Weekly upstream merge takes > 2 h on average.
- An upstream release ships an equivalent feature (then drop ours, use theirs).
- Build/iteration loop > 5 min for an incremental change.

## Out of scope (for now)

Windows/Linux builds, publishing the fork, non-PHP/JS languages, profiler/coverage UI, UML/diagram tools.
