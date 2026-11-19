# Upstream sync log

Procedure and kill criteria: `plan/13-maintenance.md`, `plan/README.md`.

| Date | Machine | Upstream | Commits | Conflicts | Time | Gate |
|---|---|---|---|---|---|---|
| 2026-11-19 | home | `4a7d10473a` | 69 | 2: `client/zed_urls.rs` (took upstream's deletion of `shared_agent_thread_url`), `onboarding/onboarding.rs` (took upstream layout, kept Zenith strings) | ≈ 15 min incl. checks | `cargo check -p zed` 1 m 14 s, 0 errors; nextest zenith_* + icons 103/103 (1 m 41 s) |

Flow used: `main` ff to `upstream/main` → merge `main` into `zenith` → merge `zenith` into `feat/look`; all three pushed. `rerere` enabled in this clone.
