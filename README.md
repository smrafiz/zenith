# Zenith

A fork of [Zed](https://github.com/zed-industries/zed) aiming at full PhpStorm/WebStorm parity for classic and agentic PHP/JS development — while keeping Zed's speed.

> Status: **planning**. No code yet. Zenith is not affiliated with Zed Industries; "Zed" is their trademark.

## Plan

Start at **[plan/README.md](plan/README.md)** — index, build order, timeline.

| Phase | Docs |
|---|---|
| 0 Foundation | 01 prerequisites · 02 architecture · 03 config layer · 15 zenith_core · 17 build · 18 performance |
| 1 Quick wins | 04 scratches · 14 toolbar UI · 05 local history · 20 templates · 27 TODO · 28 bookmarks |
| 2 Agentic | 06 IDE/MCP server · 23 agent review queue · 22 agent worktrees |
| 3 Daily depth | 21 inspections · 07 test runner · 19 WordPress · 08 HTTP client · 24 Composer/npm |
| 4 Heavy | 09 refactoring · 10 git merge/rebase · 11 Docker interpreters · 25 Laravel · 26 live templates |
| 5 Big / polish | 12 database tool · 29 settings UI · 31 PhpStorm migration · 30 profiler/coverage |
| Continuous | 13 maintenance · 16 upstream & extensions |

Progress is tracked in [Issues](../../issues) (one per plan doc) and [Milestones](../../milestones) (one per phase).

## Repositories

| Repo | Purpose |
|---|---|
| `wp-sigmadevs/zenith` (this) | plan, docs, `zed-kit` config, issue tracking |
| `wp-sigmadevs/zed` fork (to be created, see plan/01) | Zenith source code, branch `zenith` |

## Licence

- This repository (plan docs, `zed-kit` config): [MIT](LICENSE).
- Zenith fork code: follows Zed's licences (GPL-3.0 editor, AGPL-3.0 server parts, Apache-2.0 GPUI); new `zenith_*` crates are GPL-3.0-or-later.
- Standalone language servers (`wp-hooks-ls`, `laravel-ls`, …): MIT, in their own repositories.

Security issues: see [SECURITY.md](SECURITY.md).
