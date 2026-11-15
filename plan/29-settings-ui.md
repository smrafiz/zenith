# 29 — Zenith Settings UI (F11)

## Goal

Every Zenith feature configurable through a UI, not just JSON — JetBrains-style Settings dialog for Zenith sections.

First: check upstream Zed's settings UI (in progress upstream as of 2025/2026 — *verify*). If it supports registering sections from settings schemas, plug Zenith in; build our own only if not.

## Parity checklist

- [ ] Sections: one per Zenith feature (Scratches, Local History, Tests, HTTP, DB, Inspections, WordPress, Laravel, Agents, Toolbar, …) (must)
- [ ] Controls generated from settings JSON schema (bool → toggle, enum → dropdown, number, string, path picker, string list, key-value map) (must)
- [ ] Scope: User vs Project (`.zed/settings.json`) switch (must)
- [ ] Search across settings (must)
- [ ] Changes written back preserving comments/formatting (must — reuse Zed's settings-file update helpers, *verify*)
- [ ] Reset to default per setting (must)
- [ ] Per-feature "Test" buttons (e.g. DB connection test, interpreter check) (later)

## Architecture

- Crate `zenith_settings_ui`.
- Each feature's `Settings` type already provides a JSON schema (02) → generic form renderer.
- Custom widgets registered by features for complex values (DB connections editor, toolbar layout drag-drop).
- Opens as center Item "Zenith Settings" (`cmd-,` → upstream settings; `cmd-alt-,` → Zenith if separate).

## Effort

1–2 weeks (less if upstream settings UI is extensible).
