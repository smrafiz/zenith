# 18 — Performance Guard, LS Tuning, Telemetry (A6, A7, A8)

## A6 — Performance guard

Goal: prove Zenith ≈ stock Zed speed; catch regressions early.

- **Instrumentation**: every Zenith feature wraps work in `tracing` spans (`zenith_core::trace`): name, duration, thread (main vs background).
- **Main-thread budget**: any Zenith span on the main thread > 4 ms logs a warning (debug builds: also shown in perf view).
- **"Zenith: Perf" view** (debug action): table of spans (count, p50, p95, max), memory per feature store, background job queue depth.
- **Benchmark script** `zenith-bench/run.sh` (same machine, same Laravel project):
  | Metric | How |
  |---|---|
  | Cold start to first frame | launch with `--wait`-style flag / log timestamp (*verify* Zed startup timing log) |
  | Open 5k-line file, scroll | scripted, frame times from Zed's frame-time logging if available |
  | Idle memory after project open | `ps -o rss` after 60 s |
  | Memory with all panels open | same |
  | Save-to-history latency | span |
  Compare Zenith vs stock Zed of the same upstream commit; fail QA if > 10% worse.
- Add bench results to each release tag (13).

## A7 — Language server tuning profiles

Ship in `zed-kit` (03), per project type:

| Server | Setting | Purpose |
|---|---|---|
| Intelephense | `intelephense.maxMemory` (e.g. 2048), `files.exclude` (`**/node_modules`, `**/storage`, `**/var/cache`), `files.maxSize` | memory & indexing time |
| Intelephense | `stubs` minimal set per project (don't load all) | faster index |
| Phpactor | disable completion/hover where Intelephense covers it; enable only code actions + PHPStan | avoid duplicate work |
| PHPStan (via Phpactor) | run on save only, `level` from project config, memory limit | CPU spikes |
| vtsls/ESLint | `eslint.run: onSave` for large repos | typing latency |
| Zed | `file_scan_exclusions` for `vendor/**/tests`, build dirs | worktree scan |

Profiles: `laravel`, `wordpress`, `node`. Verify every key name against each server's docs.

## A8 — Telemetry

- Zed settings: `"telemetry": { "diagnostics": false, "metrics": false }` default in Zenith.
- Fork: ensure Zenith builds never report to Zed's endpoints under Zed's name (change/disable telemetry endpoint + crash reporter upload; *verify* where configured).
- Auto-update: disabled or pointed to own release feed (see 13).
- Zenith metrics stay local (perf view, optional export to JSON) — no network.

## Effort

A6: 1 week. A7: 2–3 days. A8: 1–2 days.
