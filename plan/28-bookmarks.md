# 28 — Bookmarks (F10)

## Goal

JetBrains bookmarks: anonymous and mnemonic (0–9, A–Z) bookmarks, persistent per project, with a panel.

First: check upstream Zed for bookmarks (vim marks exist in vim mode — consider reusing their storage/anchors).

## Parity checklist

- [ ] Toggle bookmark at line (`F3` JetBrains new UI / `F11` classic) (must)
- [ ] Toggle with mnemonic (`alt-F3` / `ctrl-F11`) → picker 0–9/A–Z (must)
- [ ] Jump to mnemonic `ctrl-<digit>` (must)
- [ ] Gutter icon (✓ or letter) (must)
- [ ] Bookmarks panel: list grouped by file, description editable (must)
- [ ] Anchors survive edits (use buffer anchors; re-resolve on reload by line + content hash) (must)
- [ ] Persist per workspace (store) (must)
- [ ] Next/previous bookmark (must)
- [ ] Bookmark lists (named groups) (later)

## Architecture

- Crate `zenith_bookmarks`; storage `zenith_core::store` keyed by worktree + rel path + line + line-content hash.
- Open buffers: convert to `Anchor`s for live tracking; save back line numbers on buffer save/close.
- Gutter: needs gutter decoration hook (16 upstream candidate); fallback: highlight line background via editor highlights API.

## Effort

3–4 days.
