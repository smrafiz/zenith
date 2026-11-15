# 32 — Zenith Welcome Screen

Status: ⬜ brief agreed (2026-11-16), **plan not yet written** — run `lead-engineer` with this brief first.

## Goal

One PhpStorm-style screen that **replaces both** upstream Zed first-run screens:
- Onboarding item — `crates/onboarding/src/onboarding.rs`, `basics_page.rs`
- Welcome page (no project open) — `crates/workspace/src/welcome.rs`

```
┌──────────────┬──────────────────────────┐
│ Zenith       │ [Search projects…]       │
│ Projects   ◀ │ radius-theme   ~/Sites/… │
│ Customize    │   main · 2h ago          │
│ Plugins      │ laravel-crm    ~/Code/…  │
│ Learn        │   dev · yesterday        │
│              │ [New] [Open] [Clone VCS] │
└──────────────┴──────────────────────────┘
```

## Requirements (owner-approved)

1. Left nav: **Projects** (default), **Customize**, **Plugins** (extensions), **Learn** (docs/keymap links).
2. Projects: searchable, keyboard-navigable recent projects (name, path, git branch, last opened); actions New Project / Open / Clone from VCS. WordPress/Laravel/Node templates may be a later phase.
3. Customize absorbs onboarding: theme, base keymap, import VS Code/Cursor settings, vim mode, trust-all. Reuse upstream components/logic, don't copy. "Finish setup / Skip" lives here; returning users never land on setup. Keep upstream's first-run "onboarding seen" flag semantics.
4. Telemetry: **no** "Help improve / fix Zed" toggles on this screen (Zenith ships telemetry and crash upload off). Settings stay.
5. Agent setup: Claude Agent and Codex first; Zed Agent sign-in moves into Customize.
6. Recent projects show a framework badge (WordPress / Laravel / Node) from cheap file-presence detection, off the main thread and cached; decide `zenith_core::detect` (plan 15) vs the welcome crate.
7. Logo (`VectorName::ZedLogo` → `assets/images/zed_logo.svg`, now the Zenith glyph): bolder small-size variant — sun r 5.4→8, inner peak opacity 0.45→0.7, main stroke 7.5→9. Asset-only, first chunk.

## Constraints

- New crate (e.g. `zenith_welcome`, GPL-3.0-or-later); upstream gets one-line hooks only (plan 02), ideally one redirect point.
- Never Zed name/logo. Settings key `"zenith"`.
- Fork branch: build on `feat/branding` (`0214f9dbc5`) or `zenith` after it is merged.

## lead-engineer must deliver

1. Verified upstream facts (path:line @ sha): how onboarding and welcome are registered and opened (first launch, no-project startup, actions, Help menu, restore-on-startup), recent-projects source, first-run flag key.
2. Crate plan: name, deps, modules, reused vs new.
3. Upstream hooks: files, one-line change each, count, why unavoidable.
4. Chunks in build order with owner agent, acceptance criteria, `#[gpui::test]` per chunk.
5. Risks: upstream merge churn, behaviour lost from onboarding, keyboard/a11y.
