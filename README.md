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
| `smrafiz/zenith` (this) | plan, docs, `zed-kit` config, issue tracking |
| `smrafiz/zed` fork (to be created, see plan/01) | Zenith source code, branch `zenith` |

## Licence

Plan documents: © the author, all rights reserved until decided. Zenith source code will follow Zed's licences (GPL-3.0 / AGPL-3.0 / Apache-2.0 per crate).
