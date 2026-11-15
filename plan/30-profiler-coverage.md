# 30 — Xdebug Profiler Viewer & Code Coverage (F12)

## Goal

View Xdebug profiles (cachegrind) and test coverage inside Zenith. Later-phase feature.

## Profiler — checklist

- [ ] Open `cachegrind.out.*` (Xdebug `xdebug.mode=profile`) as an Item (must)
- [ ] Views: flat function list (self/inclusive time, calls, memory), sortable; callers/callees; call tree (must)
- [ ] Jump from function → source (path mapping from 11) (must)
- [ ] Flame graph (later)
- [ ] Toggle profiling for next request (cookie/trigger `XDEBUG_TRIGGER`) via HTTP client (08) "Run with profiler" (later)

Architecture: crate `zenith_profiler`; cachegrind parser (streaming, files can be 100s MB; name compression `fn=(id)` support); results grid from `zenith_core::ui`; parse in background, show progress.

## Coverage — checklist

- [ ] Run tests with coverage (07): PHPUnit `--coverage-clover`, Pest `--coverage-clover`, Jest/Vitest `--coverage --coverageReporters=lcov` (must)
- [ ] Gutter: covered/uncovered/partial line marks (must)
- [ ] Coverage panel: % per dir/file, sortable (must)
- [ ] Coverage for changed lines only (diff coverage) (later)

Architecture: crate `zenith_coverage`; Clover XML + LCOV parsers → per-file line maps; gutter via decoration hook (16) or line highlights; requires pcov/Xdebug coverage in interpreter (11).

## Tests

Parser fixtures (real cachegrind, clover, lcov); large-file performance test (500 MB cachegrind parse < 30 s target).

## Effort

Profiler 2 weeks; coverage 1–2 weeks.
